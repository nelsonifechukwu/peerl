"""
LLM Service: GPT-4 integration for facilitation and coaching
Implements both LLM-Only Facilitator and Rotating Anchor coaching
"""
import openai
from typing import List, Dict
from config import OPENAI_API_KEY, OPENAI_MODEL

openai.api_key = OPENAI_API_KEY

class LLMService:
    """Handles all LLM interactions"""
    
    def __init__(self, condition: str, topic: str):
        self.condition = condition
        self.topic = topic
        self.conversation_history: List[Dict] = []
    
    async def generate_llm_only_response(self, discussion_history: List[Dict], challenge_question: str) -> str:
        """Generate LLM Facilitator response (LLM-Only condition)"""
        
        system_prompt = f"""You are facilitating a collaborative learning discussion on "{self.topic}". Your role is to:
1. Ask open-ended questions that probe deeper reasoning
2. Connect different participants' contributions
3. Encourage quieter members to participate
4. Synthesize key points periodically
5. Keep discussion focused on the challenge question

Be concise (1-2 sentences). Sound natural and supportive, not robotic.

Challenge Question for this discussion:
{challenge_question}

Facilitation behaviors to use:
- Opening: Start with an inviting question
- Probing: "Can you explain your reasoning?", "What makes you say that?"
- Connecting: "How does that relate to what [person] said earlier?"
- Encouraging: "We haven't heard from you yet - what's your take?"
- Synthesizing: "So it sounds like we're seeing a pattern..."
- Closing: Summarize key insights before moving to quiz
"""
        
        # Build messages for API call
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent discussion history (last 10 messages)
        recent_history = discussion_history[-10:] if len(discussion_history) > 10 else discussion_history
        for msg in recent_history:
            role = "assistant" if msg["sender"] == "LLM Facilitator" else "user"
            content = f"{msg['sender']}: {msg['content']}"
            messages.append({"role": role, "content": content})
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=150,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM API Error: {e}")
            # Fallback facilitation
            return "What are your thoughts on the tradeoffs here?"
    
    async def generate_anchor_coaching(self, 
                                      anchor_name: str,
                                      discussion_history: List[Dict],
                                      challenge_question: str,
                                      time_remaining_mins: int) -> str:
        """Generate private coaching for current anchor (Rotating Anchor condition)"""
        
        system_prompt = f"""You are coaching {anchor_name} who is currently facilitating a learning discussion on "{self.topic}".

Your role: Provide PRIVATE coaching suggestions (only {anchor_name} sees these). Suggest:
1. Specific questions to ask the group
2. Strategies to encourage participation from quieter members
3. Ways to deepen the discussion or connect ideas

Be ultra-concise (1 short suggestion). Format as actionable advice.

Challenge Question being discussed:
{challenge_question}

Time remaining in this anchor's turn: {time_remaining_mins} minutes

Examples of good coaching:
- "Ask: 'Does anyone disagree with that reasoning?'"
- "Someone hasn't spoken yet - invite them: '[Name], what's your perspective?'"
- "Probe deeper: 'What's the downside of that approach?'"
- "Summarize what's been said so far, then ask for other viewpoints"
"""
        
        # Recent discussion for context
        recent_history = discussion_history[-5:] if len(discussion_history) > 5 else discussion_history
        messages = [{"role": "system", "content": system_prompt}]
        
        context = "Recent discussion:\n" + "\n".join([
            f"{msg['sender']}: {msg['content']}" for msg in recent_history
        ])
        messages.append({"role": "user", "content": context})
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=80,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Coaching Error: {e}")
            # Fallback coaching
            return "Ask the group: 'What are the tradeoffs we should consider?'"
    
    async def generate_anchor_feedback(self,
                                      anchor_name: str,
                                      discussion_history: List[Dict],
                                      anchor_duration_mins: int) -> str:
        """Generate personalized feedback after anchor's turn"""
        
        # Count anchor's facilitation moves
        anchor_messages = [
            msg for msg in discussion_history 
            if msg["sender"] == anchor_name and msg.get("is_anchor", False)
        ]
        
        system_prompt = f"""You are providing brief, personalized feedback to {anchor_name} who just finished facilitating a discussion.

They facilitated for {anchor_duration_mins} minutes and made {len(anchor_messages)} facilitation moves.

Give 1-2 sentences of constructive feedback:
1. Highlight ONE thing they did well
2. Suggest ONE area for improvement (be kind and specific)

Tone: Encouraging and supportive, like a helpful peer coach.

Examples:
- "Nice job asking open-ended questions! Next time, try connecting different people's ideas together."
- "Great encouragement of participation! Consider probing deeper on the 'why' behind people's answers."
- "Good synthesis of ideas! You could also invite quieter members to share more."
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Anchor {anchor_name} facilitated these messages: " + str(anchor_messages)}
        ]
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=100,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Feedback Error: {e}")
            return "Nice facilitation! Keep encouraging everyone to participate."
