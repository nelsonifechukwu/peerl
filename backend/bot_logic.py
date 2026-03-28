"""
AI Bot Logic: Simulates realistic peer learner behavior
Based on HCI research on bot detection avoidance
"""
import random
import asyncio
from typing import List, Dict
from config import BOT_NAMES, BOT_RESPONSE_DELAY_MIN, BOT_RESPONSE_DELAY_MAX
from config import BOT_AFFIRMATION_PROB, BOT_QUESTION_PROB, BOT_CONTRIBUTION_PROB

class BotPersonality:
    """Different personality traits for each bot"""
    def __init__(self, name: str):
        self.name = name
        if name == "Alex":
            # Alex: More questioning, slightly hesitant
            self.question_boost = 1.2  # 20% more likely to ask questions
            self.contribution_style = "tentative"  # "I think maybe...", "Could it be..."
            self.filler_words = ["hmm", "wait", "let me think"]
        else:  # Jordan
            # Jordan: More confident, makes small mistakes
            self.question_boost = 0.8  # 20% less likely to ask questions
            self.contribution_style = "confident"  # "I believe...", "It seems clear that..."
            self.filler_words = ["oh", "actually", "interesting"]

class BotBehavior:
    """Generates realistic bot responses"""
    
    def __init__(self, bot_name: str, topic: str, condition: str):
        self.personality = BotPersonality(bot_name)
        self.topic = topic
        self.condition = condition
        self.message_count = 0
        
    async def get_response_delay(self) -> int:
        """Random delay between BOT_RESPONSE_DELAY_MIN and BOT_RESPONSE_DELAY_MAX seconds"""
        return random.randint(BOT_RESPONSE_DELAY_MIN, BOT_RESPONSE_DELAY_MAX)
    
    def should_respond(self, recent_messages: List[Dict], current_speaker: str = None) -> bool:
        """Decide if bot should respond based on context"""
        # Don't respond if we just spoke
        if recent_messages and recent_messages[-1].get("sender") == self.personality.name:
            return False
        
        # Don't respond during anchor's turn if we're not the anchor (Rotating Anchor condition)
        if self.condition == "rotating_anchor" and current_speaker and current_speaker != self.personality.name:
            # Still respond occasionally (10% chance) to seem natural
            return random.random() < 0.1
        
        # Higher chance to respond if someone asked a question
        if recent_messages and "?" in recent_messages[-1].get("content", ""):
            return random.random() < 0.7
        
        # Base response probability
        return random.random() < 0.4
    
    def generate_response(self, discussion_context: str, recent_messages: List[Dict], is_anchor: bool = False) -> str:
        """Generate realistic bot response based on role and context"""
        
        if is_anchor:
            # Bot is facilitating - ask open questions, encourage participation
            return self._generate_anchor_response(discussion_context, recent_messages)
        
        # Regular participant behavior
        response_type = self._choose_response_type()
        
        if response_type == "affirmation":
            return self._generate_affirmation(recent_messages)
        elif response_type == "question":
            return self._generate_question(discussion_context, recent_messages)
        else:  # contribution
            return self._generate_contribution(discussion_context, recent_messages)
    
    def _choose_response_type(self) -> str:
        """Choose response type based on probabilities"""
        adjusted_question_prob = BOT_QUESTION_PROB * self.personality.question_boost
        
        # Normalize probabilities
        total = BOT_AFFIRMATION_PROB + adjusted_question_prob + BOT_CONTRIBUTION_PROB
        affirmation_prob = BOT_AFFIRMATION_PROB / total
        question_prob = adjusted_question_prob / total
        
        rand = random.random()
        if rand < affirmation_prob:
            return "affirmation"
        elif rand < affirmation_prob + question_prob:
            return "question"
        else:
            return "contribution"
    
    def _generate_affirmation(self, recent_messages: List[Dict]) -> str:
        """Generate affirming response"""
        affirmations = [
            "That makes sense!",
            "Good point",
            "I agree with that",
            "Yeah, I see what you mean",
            "That's a fair way to think about it",
            f"{random.choice(self.personality.filler_words)}, yeah that tracks",
            "I hadn't thought of it that way but you're right",
        ]
        return random.choice(affirmations)
    
    def _generate_question(self, context: str, recent_messages: List[Dict]) -> str:
        """Generate clarifying or probing question"""
        if self.personality.contribution_style == "tentative":
            questions = [
                "Wait, can you explain that again?",
                "Hmm, I'm not sure I follow - why would that be better?",
                "What about the opposite case though?",
                "Could you give an example of that?",
                "How does that connect to what we read earlier?",
            ]
        else:  # confident
            questions = [
                "But what about the tradeoffs?",
                "Okay, but wouldn't that cause problems with...?",
                "How would that work in practice though?",
                "What's the downside of that approach?",
                "Interesting - can someone build on that?",
            ]
        return random.choice(questions)
    
    def _generate_contribution(self, context: str, recent_messages: List[Dict]) -> str:
        """Generate content contribution"""
        # Topic-specific contributions
        if "lazy_eager" in self.topic:
            contributions = self._get_lazy_eager_contributions()
        else:  # parallelism topic
            contributions = self._get_parallelism_contributions()
        
        # Add personality flavoring
        contribution = random.choice(contributions)
        if self.personality.contribution_style == "tentative" and random.random() < 0.3:
            contribution = f"{random.choice(self.personality.filler_words)}, {contribution}"
        
        # Occasionally make a small mistake that gets corrected
        if random.random() < 0.15:  # 15% chance of self-correction
            mistake_starters = [
                "Oh wait, I meant",
                "Actually,",
                "Hmm no, ",
            ]
            contribution = f"{random.choice(mistake_starters)} {contribution}"
        
        return contribution
    
    def _get_lazy_eager_contributions(self) -> List[str]:
        """Topic-specific contributions for lazy vs eager"""
        return [
            "I think eager makes sense when you know you'll use everything",
            "Lazy seems better when memory is limited",
            "The library example helped - it's like not shelving books until someone needs them",
            "For the climate data, lazy seems obvious since we only need a tiny fraction",
            "But eager could be faster if we're going to access all the data eventually",
            "It depends on the access pattern, right?",
            "I'm thinking about streaming - that's definitely lazy",
            "So the tradeoff is upfront cost vs ongoing cost",
        ]
    
    def _get_parallelism_contributions(self) -> List[str]:
        """Topic-specific contributions for parallelism"""
        return [
            "Shared-memory makes coordination easier but creates conflicts",
            "Independent is safer but harder to combine results",
            "The kitchen example makes it clear - shared workspace vs separate kitchens",
            "For the news analysis, independent might be better to avoid conflicts",
            "But combining 10 lists at the end could be slow",
            "I think shared-memory is worth it when tasks need to coordinate a lot",
            "Independent parallelism is like divide-and-conquer",
            "The main question is: do the tasks need to communicate or not?",
        ]
    
    def _generate_anchor_response(self, context: str, recent_messages: List[Dict]) -> str:
        """Generate facilitation response when bot is the anchor"""
        # These would normally come from LLM coaching, but bots use scripted facilitation
        facilitation_moves = [
            "What do others think about that point?",
            "Can someone build on that idea?",
            "Let's make sure everyone weighs in - any other perspectives?",
            "Good discussion so far. How does this connect to the challenge question?",
            "I want to hear from everyone - anyone else have thoughts?",
            "Let's dig deeper into that tradeoff",
        ]
        return random.choice(facilitation_moves)

# Bot instances
def create_bots(topic: str, condition: str) -> Dict[str, BotBehavior]:
    """Create bot instances for the session"""
    return {
        name: BotBehavior(name, topic, condition)
        for name in BOT_NAMES
    }
