"""
Database models for peer learning platform
Stores all experimental data as specified in CW2
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Participant(Base):
    """Participant information (anonymized as P001-P016)"""
    __tablename__ = "participants"
    
    id = Column(String, primary_key=True)  # P001, P002, etc.
    group_number = Column(Integer, nullable=False)  # 1-4 for counterbalancing
    name = Column(String, nullable=False)  # Display name (not stored in final analysis)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_debrief_consent = Column(Boolean, default=None)  # Confirmed after debrief
    
    sessions = relationship("Session", back_populates="participant")
    final_preference = relationship("FinalPreference", back_populates="participant", uselist=False)

class Session(Base):
    """Individual module session (2 per participant)"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String, ForeignKey("participants.id"), nullable=False)
    module_number = Column(Integer, nullable=False)  # 1 or 2
    condition = Column(String, nullable=False)  # llm_only or rotating_anchor
    topic = Column(String, nullable=False)  # lazy_eager_evaluation or shared_independent_parallelism
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, default=None)
    
    participant = relationship("Participant", back_populates="sessions")
    messages = relationship("Message", back_populates="session")
    quiz_responses = relationship("QuizResponse", back_populates="session")
    reflection = relationship("Reflection", back_populates="session", uselist=False)

class Message(Base):
    """Chat messages during discussion"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender = Column(String, nullable=False)  # Participant name, "Alex", "Jordan", or "LLM Facilitator"
    sender_type = Column(String, nullable=False)  # "participant", "bot", "llm_facilitator", "llm_coach"
    content = Column(Text, nullable=False)
    is_private = Column(Boolean, default=False)  # True for LLM coaching messages
    
    session = relationship("Session", back_populates="messages")

class QuizResponse(Base):
    """Quiz responses after each module"""
    __tablename__ = "quiz_responses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    question_number = Column(Integer, nullable=False)  # 1-6
    selected_answer = Column(String, nullable=False)  # A, B, C, or D
    is_correct = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("Session", back_populates="quiz_responses")

class Reflection(Base):
    """Post-module reflection"""
    __tablename__ = "reflections"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    effectiveness_text = Column(Text, nullable=False)  # "How effectively did this format help you?"
    helpful_aspects_text = Column(Text, nullable=False)  # "What was most/least helpful?"
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("Session", back_populates="reflection")

class FinalPreference(Base):
    """Final comparative assessment after both modules"""
    __tablename__ = "final_preferences"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String, ForeignKey("participants.id"), nullable=False)
    preferred_condition = Column(String, nullable=False)  # llm_only, rotating_anchor, or both_equal
    explanation = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    participant = relationship("Participant", back_populates="final_preference")
