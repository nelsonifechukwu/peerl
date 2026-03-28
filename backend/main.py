"""
FastAPI Backend for Peer Learning Platform
Handles all session logic, bot responses, LLM integration, and data logging
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import asyncio
import json
import random

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from database import Base, Participant, Session as DBSession, Message, QuizResponse, Reflection, FinalPreference
from config import (
    DATABASE_URL, COUNTERBALANCING, PARTICIPANT_ID_FORMAT,
    Condition, Topic, NUM_PARTICIPANTS, ANCHOR_ROTATION_MINS,
    DISCUSSION_LO_MINS, DISCUSSION_RA_MINS
)
from content import CONTENT
from bot_logic import create_bots
from llm_service import LLMService

# FastAPI app
app = FastAPI(title="Peer Learning Platform")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Pydantic models for requests/responses
class ParticipantCreate(BaseModel):
    name: str

class ParticipantResponse(BaseModel):
    participant_id: str
    name: str
    group_number: int
    module1_condition: str
    module1_topic: str
    module2_condition: str
    module2_topic: str

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    timestamp: datetime
    sender: str
    sender_type: str
    content: str
    is_private: bool

class QuizSubmit(BaseModel):
    responses: List[Dict[str, str]]  # [{"question_number": 1, "selected_answer": "A"}, ...]

class ReflectionSubmit(BaseModel):
    effectiveness_text: str
    helpful_aspects_text: str

class FinalPreferenceSubmit(BaseModel):
    preferred_condition: str  # llm_only, rotating_anchor, or both_equal
    explanation: str

class SessionState(BaseModel):
    """Current state of the session"""
    participant_id: str
    module_number: int
    condition: str
    topic: str
    phase: str  # intro, priming, discussion, quiz, reflection, rest, final_choice, complete
    time_remaining_seconds: int
    current_anchor: Optional[str] = None  # For rotating anchor condition
    anchor_rotation_number: Optional[int] = None  # 1, 2, or 3

# In-memory session manager
class SessionManager:
    """Manages active sessions and bot responses"""
    def __init__(self):
        self.active_sessions: Dict[str, Dict] = {}  # participant_id -> session_data
        self.bot_tasks: Dict[str, asyncio.Task] = {}  # session_id -> bot task
    
    def create_session(self, participant_id: str, module_number: int, condition: str, topic: str):
        """Initialize session state"""
        session_key = f"{participant_id}_module{module_number}"
        self.active_sessions[session_key] = {
            "participant_id": participant_id,
            "module_number": module_number,
            "condition": condition,
            "topic": topic,
            "phase": "intro",
            "start_time": datetime.utcnow(),
            "discussion_start_time": None,
            "current_anchor": None,
            "anchor_rotation_number": 0,
            "anchor_start_time": None,
            "bots": create_bots(topic, condition),
            "llm_service": LLMService(condition, topic),
            "discussion_history": [],
        }
        return session_key
    
    def get_session(self, session_key: str) -> Optional[Dict]:
        """Get session data"""
        return self.active_sessions.get(session_key)
    
    def update_phase(self, session_key: str, new_phase: str):
        """Update session phase"""
        if session_key in self.active_sessions:
            self.active_sessions[session_key]["phase"] = new_phase
    
    def end_session(self, session_key: str):
        """Clean up session"""
        if session_key in self.active_sessions:
            del self.active_sessions[session_key]
        if session_key in self.bot_tasks:
            self.bot_tasks[session_key].cancel()
            del self.bot_tasks[session_key]

session_manager = SessionManager()

# Startup/shutdown
@app.on_event("startup")
async def startup():
    """Create database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    """Clean up"""
    await engine.dispose()

# Health check
@app.get("/")
async def root():
    return {"status": "Peer Learning Platform API Running"}

# Participant endpoints
@app.post("/api/participants", response_model=ParticipantResponse)
async def create_participant(participant_data: ParticipantCreate):
    """Create new participant and assign to counterbalancing group"""
    async with async_session_maker() as db:
        # Count existing participants to determine next ID and group
        from sqlalchemy import select, func
        result = await db.execute(select(func.count(Participant.id)))
        count = result.scalar() or 0
        
        # Generate participant ID (P001, P002, etc.)
        participant_id = PARTICIPANT_ID_FORMAT.format(count + 1)
        
        # Assign to counterbalancing group (round-robin across groups 1-4)
        group_number = (count % 4) + 1
        
        # Get counterbalancing configuration
        config = COUNTERBALANCING[group_number]
        module1_condition, module1_topic, module2_condition, module2_topic = config
        
        # Create participant
        participant = Participant(
            id=participant_id,
            group_number=group_number,
            name=participant_data.name
        )
        
        db.add(participant)
        await db.commit()
        await db.refresh(participant)
        
        return ParticipantResponse(
            participant_id=participant.id,
            name=participant.name,
            group_number=participant.group_number,
            module1_condition=module1_condition.value,
            module1_topic=module1_topic.value,
            module2_condition=module2_condition.value,
            module2_topic=module2_topic.value,
        )

@app.get("/api/participants/{participant_id}", response_model=ParticipantResponse)
async def get_participant(participant_id: str):
    """Get participant info"""
    async with async_session_maker() as db:
        result = await db.execute(
            select(Participant).where(Participant.id == participant_id)
        )
        participant = result.scalar_one_or_none()
        
        if not participant:
            raise HTTPException(status_code=404, detail="Participant not found")
        
        # Get counterbalancing config
        config = COUNTERBALANCING[participant.group_number]
        module1_condition, module1_topic, module2_condition, module2_topic = config
        
        return ParticipantResponse(
            participant_id=participant.id,
            name=participant.name,
            group_number=participant.group_number,
            module1_condition=module1_condition.value,
            module1_topic=module1_topic.value,
            module2_condition=module2_condition.value,
            module2_topic=module2_topic.value,
        )

# Session endpoints
@app.post("/api/sessions/start")
async def start_session(participant_id: str, module_number: int):
    """Start a new module session"""
    async with async_session_maker() as db:
        # Get participant and their counterbalancing
        result = await db.execute(
            select(Participant).where(Participant.id == participant_id)
        )
        participant = result.scalar_one_or_none()
        
        if not participant:
            raise HTTPException(status_code=404, detail="Participant not found")
        
        # Get condition and topic for this module
        config = COUNTERBALANCING[participant.group_number]
        if module_number == 1:
            condition, topic = config[0], config[1]
        else:
            condition, topic = config[2], config[3]
        
        # Create database session record
        db_session = DBSession(
            participant_id=participant_id,
            module_number=module_number,
            condition=condition.value,
            topic=topic.value,
        )
        db.add(db_session)
        await db.commit()
        await db.refresh(db_session)
        
        # Create in-memory session manager state
        session_key = session_manager.create_session(
            participant_id, module_number, condition.value, topic.value
        )
        
        return {
            "session_id": db_session.id,
            "session_key": session_key,
            "condition": condition.value,
            "topic": topic.value,
            "module_number": module_number
        }

@app.get("/api/content/{topic}")
async def get_content(topic: str):
    """Get priming text, challenge question, and quiz for a topic"""
    if topic not in CONTENT:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return {
        "title": CONTENT[topic]["title"],
        "priming_text": CONTENT[topic]["priming_text"],
        "challenge_question": CONTENT[topic]["challenge_question"],
        "quiz": CONTENT[topic]["quiz"]
    }

# Message endpoints
@app.post("/api/sessions/{session_key}/messages", response_model=MessageResponse)
async def send_message(session_key: str, message_data: MessageCreate):
    """Participant sends a message"""
    session = session_manager.get_session(session_key)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    participant_id = session["participant_id"]
    
    async with async_session_maker() as db:
        # Get participant name
        result = await db.execute(
            select(Participant).where(Participant.id == participant_id)
        )
        participant = result.scalar_one()
        
        # Get database session
        result = await db.execute(
            select(DBSession).where(
                DBSession.participant_id == participant_id,
                DBSession.module_number == session["module_number"]
            )
        )
        db_session = result.scalar_one()
        
        # Save message
        msg = Message(
            session_id=db_session.id,
            sender=participant.name,
            sender_type="participant",
            content=message_data.content,
            is_private=False
        )
        db.add(msg)
        await db.commit()
        await db.refresh(msg)
        
        # Add to session history
        session["discussion_history"].append({
            "sender": participant.name,
            "content": message_data.content,
            "timestamp": msg.timestamp,
            "sender_type": "participant"
        })
        
        # Trigger bot responses
        asyncio.create_task(generate_bot_responses(session_key, db_session.id))
        
        # If LLM-Only condition, maybe trigger LLM response
        if session["condition"] == Condition.LLM_ONLY.value:
            asyncio.create_task(generate_llm_facilitator_response(session_key, db_session.id))
        
        return MessageResponse(
            id=msg.id,
            timestamp=msg.timestamp,
            sender=msg.sender,
            sender_type=msg.sender_type,
            content=msg.content,
            is_private=msg.is_private
        )

@app.get("/api/sessions/{session_key}/messages", response_model=List[MessageResponse])
async def get_messages(session_key: str):
    """Get all messages for a session"""
    session = session_manager.get_session(session_key)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    async with async_session_maker() as db:
        result = await db.execute(
            select(DBSession).where(
                DBSession.participant_id == session["participant_id"],
                DBSession.module_number == session["module_number"]
            )
        )
        db_session = result.scalar_one()
        
        result = await db.execute(
            select(Message).where(Message.session_id == db_session.id).order_by(Message.timestamp)
        )
        messages = result.scalars().all()
        
        return [
            MessageResponse(
                id=msg.id,
                timestamp=msg.timestamp,
                sender=msg.sender,
                sender_type=msg.sender_type,
                content=msg.content,
                is_private=msg.is_private
            )
            for msg in messages
        ]

# Bot response generation (background tasks)
async def generate_bot_responses(session_key: str, db_session_id: int):
    """Generate bot responses with realistic delays"""
    session = session_manager.get_session(session_key)
    if not session:
        return
    
    # Each bot decides if it should respond
    for bot_name, bot in session["bots"].items():
        should_respond = bot.should_respond(
            session["discussion_history"],
            session.get("current_anchor")
        )
        
        if should_respond:
            # Wait realistic delay
            delay = await bot.get_response_delay()
            await asyncio.sleep(delay)
            
            # Generate response
            is_anchor = (session.get("current_anchor") == bot_name)
            response = bot.generate_response(
                discussion_context=CONTENT[session["topic"]]["challenge_question"],
                recent_messages=session["discussion_history"],
                is_anchor=is_anchor
            )
            
            # Save to database
            async with async_session_maker() as db:
                msg = Message(
                    session_id=db_session_id,
                    sender=bot_name,
                    sender_type="bot",
                    content=response,
                    is_private=False
                )
                db.add(msg)
                await db.commit()
                
                # Add to history
                session["discussion_history"].append({
                    "sender": bot_name,
                    "content": response,
                    "timestamp": msg.timestamp,
                    "sender_type": "bot"
                })

async def generate_llm_facilitator_response(session_key: str, db_session_id: int):
    """Generate LLM facilitator response (LLM-Only condition)"""
    session = session_manager.get_session(session_key)
    if not session or session["condition"] != Condition.LLM_ONLY.value:
        return
    
    # Don't respond to every message - be selective
    if len(session["discussion_history"]) % 3 != 0:  # Respond every 3 messages
        return
    
    # Wait a bit (LLM facilitator responds slightly faster than bots)
    await asyncio.sleep(random.randint(20, 40))
    
    # Generate response
    llm_service = session["llm_service"]
    response = await llm_service.generate_llm_only_response(
        session["discussion_history"],
        CONTENT[session["topic"]]["challenge_question"]
    )
    
    # Save to database
    async with async_session_maker() as db:
        msg = Message(
            session_id=db_session_id,
            sender="LLM Facilitator",
            sender_type="llm_facilitator",
            content=response,
            is_private=False
        )
        db.add(msg)
        await db.commit()
        
        # Add to history
        session["discussion_history"].append({
            "sender": "LLM Facilitator",
            "content": response,
            "timestamp": msg.timestamp,
            "sender_type": "llm_facilitator"
        })

# Rotating anchor management
@app.post("/api/sessions/{session_key}/rotate-anchor")
async def rotate_anchor(session_key: str):
    """Rotate to next anchor (Rotating Anchor condition only)"""
    session = session_manager.get_session(session_key)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["condition"] != Condition.ROTATING_ANCHOR.value:
        raise HTTPException(status_code=400, detail="Not in Rotating Anchor condition")
    
    # Determine next anchor
    anchor_sequence = [session["participant_id"]] + list(session["bots"].keys())
    current_rotation = session["anchor_rotation_number"]
    next_rotation = current_rotation + 1
    
    if next_rotation >= len(anchor_sequence):
        # All rotations complete
        return {"anchor_rotation_complete": True}
    
    next_anchor = anchor_sequence[next_rotation]
    session["current_anchor"] = next_anchor
    session["anchor_rotation_number"] = next_rotation
    session["anchor_start_time"] = datetime.utcnow()
    
    # If participant is next anchor, send them coaching
    is_participant_anchor = (next_anchor == session["participant_id"])
    
    return {
        "current_anchor": next_anchor,
        "rotation_number": next_rotation + 1,
        "total_rotations": len(anchor_sequence),
        "is_participant_anchor": is_participant_anchor
    }

@app.get("/api/sessions/{session_key}/coaching")
async def get_anchor_coaching(session_key: str):
    """Get LLM coaching for current anchor"""
    session = session_manager.get_session(session_key)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["condition"] != Condition.ROTATING_ANCHOR.value:
        raise HTTPException(status_code=400, detail="Not in Rotating Anchor condition")
    
    if session["current_anchor"] != session["participant_id"]:
        raise HTTPException(status_code=403, detail="You are not the current anchor")
    
    # Calculate time remaining in anchor turn
    if session["anchor_start_time"]:
        elapsed = (datetime.utcnow() - session["anchor_start_time"]).total_seconds() / 60
        time_remaining = max(0, ANCHOR_ROTATION_MINS - elapsed)
    else:
        time_remaining = ANCHOR_ROTATION_MINS
    
    # Generate coaching
    llm_service = session["llm_service"]
    coaching = await llm_service.generate_anchor_coaching(
        anchor_name=session["current_anchor"],
        discussion_history=session["discussion_history"],
        challenge_question=CONTENT[session["topic"]]["challenge_question"],
        time_remaining_mins=int(time_remaining)
    )
    
    # Save as private message
    async with async_session_maker() as db:
        result = await db.execute(
            select(DBSession).where(
                DBSession.participant_id == session["participant_id"],
                DBSession.module_number == session["module_number"]
            )
        )
        db_session = result.scalar_one()
        
        msg = Message(
            session_id=db_session.id,
            sender="LLM Coach",
            sender_type="llm_coach",
            content=coaching,
            is_private=True
        )
        db.add(msg)
        await db.commit()
    
    return {"coaching": coaching}

# Quiz endpoints
@app.post("/api/sessions/{session_key}/quiz")
async def submit_quiz(session_key: str, quiz_data: QuizSubmit):
    """Submit quiz responses"""
    session = session_manager.get_session(session_key)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    async with async_session_maker() as db:
        # Get database session
        result = await db.execute(
            select(DBSession).where(
                DBSession.participant_id == session["participant_id"],
                DBSession.module_number == session["module_number"]
            )
        )
        db_session = result.scalar_one()
        
        # Get correct answers
        quiz_questions = CONTENT[session["topic"]]["quiz"]
        
        # Save each response
        for response in quiz_data.responses:
            q_num = int(response["question_number"])
            selected = response["selected_answer"]
            
            # Find correct answer
            correct_answer = quiz_questions[q_num - 1]["correct"]
            is_correct = (selected == correct_answer)
            
            quiz_response = QuizResponse(
                session_id=db_session.id,
                question_number=q_num,
                selected_answer=selected,
                is_correct=is_correct
            )
            db.add(quiz_response)
        
        await db.commit()
        
        # Calculate score
        correct_count = sum(1 for r in quiz_data.responses 
                          if r["selected_answer"] == quiz_questions[int(r["question_number"]) - 1]["correct"])
        score_percentage = (correct_count / len(quiz_data.responses)) * 100
        
        return {
            "score_percentage": score_percentage,
            "correct_count": correct_count,
            "total_questions": len(quiz_data.responses)
        }

# Reflection endpoints
@app.post("/api/sessions/{session_key}/reflection")
async def submit_reflection(session_key: str, reflection_data: ReflectionSubmit):
    """Submit post-module reflection"""
    session = session_manager.get_session(session_key)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    async with async_session_maker() as db:
        # Get database session
        result = await db.execute(
            select(DBSession).where(
                DBSession.participant_id == session["participant_id"],
                DBSession.module_number == session["module_number"]
            )
        )
        db_session = result.scalar_one()
        
        # Mark session as complete
        db_session.end_time = datetime.utcnow()
        
        # Save reflection
        reflection = Reflection(
            session_id=db_session.id,
            effectiveness_text=reflection_data.effectiveness_text,
            helpful_aspects_text=reflection_data.helpful_aspects_text
        )
        db.add(reflection)
        await db.commit()
    
    # Clean up in-memory session
    session_manager.end_session(session_key)
    
    return {"status": "reflection_saved"}

# Final preference endpoints
@app.post("/api/participants/{participant_id}/final-preference")
async def submit_final_preference(participant_id: str, preference_data: FinalPreferenceSubmit):
    """Submit final comparative preference after both modules"""
    async with async_session_maker() as db:
        # Check participant exists
        result = await db.execute(
            select(Participant).where(Participant.id == participant_id)
        )
        participant = result.scalar_one_or_none()
        
        if not participant:
            raise HTTPException(status_code=404, detail="Participant not found")
        
        # Save preference
        preference = FinalPreference(
            participant_id=participant_id,
            preferred_condition=preference_data.preferred_condition,
            explanation=preference_data.explanation
        )
        db.add(preference)
        await db.commit()
        
        return {"status": "preference_saved"}

# Data export endpoint
@app.get("/api/data/export")
async def export_data():
    """Export all data for analysis (CSV format)"""
    async with async_session_maker() as db:
        # Get all data
        participants = await db.execute(select(Participant))
        sessions = await db.execute(select(DBSession))
        messages = await db.execute(select(Message))
        quizzes = await db.execute(select(QuizResponse))
        reflections = await db.execute(select(Reflection))
        preferences = await db.execute(select(FinalPreference))
        
        return {
            "participants": [dict(p.__dict__) for p in participants.scalars()],
            "sessions": [dict(s.__dict__) for s in sessions.scalars()],
            "messages": [dict(m.__dict__) for m in messages.scalars()],
            "quiz_responses": [dict(q.__dict__) for q in quizzes.scalars()],
            "reflections": [dict(r.__dict__) for r in reflections.scalars()],
            "final_preferences": [dict(p.__dict__) for p in preferences.scalars()],
        }
