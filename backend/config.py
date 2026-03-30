"""
Configuration for Peer Learning Platform
Implements the exact protocol from CW2
"""
import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4-1106-preview"  # GPT-4 Turbo

# Session Structure (minutes)
PLATFORM_INTRO_MINS = 1
INFO_PRIMING_LO_MINS = 3  # LLM-Only gets 3 mins
INFO_PRIMING_RA_MINS = 2  # Rotating Anchor gets 2 mins
DISCUSSION_LO_MINS = 8    # LLM-Only discussion
DISCUSSION_RA_MINS = 9    # Rotating Anchor discussion (3x3 min rotations)
QUIZ_MINS = 2
REFLECTION_MINS = 2
FINAL_CHOICE_MINS = 2
REST_BETWEEN_MODULES_SECS = 60  # 1 minute rest

# Rotating Anchor Settings
ANCHOR_ROTATION_MINS = 3  # Each participant facilitates for 3 mins
NUM_PARTICIPANTS = 3       # Real participant + 2 bots

# Bot Behavior Parameters (from research)
BOT_RESPONSE_DELAY_MIN = 5  # seconds
BOT_RESPONSE_DELAY_MAX = 10  # seconds
BOT_AFFIRMATION_PROB = 0.70  # 70% affirm
BOT_QUESTION_PROB = 0.20     # 20% ask questions
BOT_CONTRIBUTION_PROB = 0.10 # 10% contribute new ideas

# Bot Names (gender-neutral)
BOT_NAMES = ["Alex", "Jordan"]

# Topics
class Topic(str, Enum):
    LAZY_EAGER = "lazy_eager_evaluation"
    PARALLEL = "shared_independent_parallelism"

# Conditions
class Condition(str, Enum):
    LLM_ONLY = "llm_only"
    ROTATING_ANCHOR = "rotating_anchor"

# Counterbalancing Groups (N=4 each)
# Group structure: (Module1_Condition, Module1_Topic, Module2_Condition, Module2_Topic)
COUNTERBALANCING = {
    1: (Condition.LLM_ONLY, Topic.LAZY_EAGER, Condition.ROTATING_ANCHOR, Topic.PARALLEL),
    2: (Condition.LLM_ONLY, Topic.PARALLEL, Condition.ROTATING_ANCHOR, Topic.LAZY_EAGER),
    3: (Condition.ROTATING_ANCHOR, Topic.LAZY_EAGER, Condition.LLM_ONLY, Topic.PARALLEL),
    4: (Condition.ROTATING_ANCHOR, Topic.PARALLEL, Condition.LLM_ONLY, Topic.LAZY_EAGER),
}

# Database
DATABASE_URL = "sqlite+aiosqlite:///./peer_learning.db"

# Participant ID format
PARTICIPANT_ID_FORMAT = "P{:03d}"  # P001, P002, etc.
