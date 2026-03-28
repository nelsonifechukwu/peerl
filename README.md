# Peer Learning Platform - Complete Implementation Guide

**Study:** LLM-Facilitated vs Peer-Facilitated Collaborative Learning
**For:** Cambridge MPhil HCI Coursework 3
**Researcher:** Nelson Elijah (Matthew)

---

## Platform Overview

This is a production-ready experimental platform implementing your CW2 protocol exactly:
- **N=16 participants** (P001-P016)
- **Within-subjects design** (each participant experiences both conditions)
- **2 AI bots** simulating peer learners (Alex & Jordan)
- **34-minute session** per participant
- **4 counterbalanced groups**
- **2 topics:** Lazy vs Eager Evaluation, Shared-Memory vs Independent Parallelism
- **2 conditions:** LLM-Only Facilitator, Rotating Anchor with LLM Coaching

---

## Technology Stack

**Backend:**
- FastAPI (Python async web framework)
- SQLite database (all data logged automatically)
- GPT-4 API (facilitation & coaching)
- Realistic bot behavior (based on HCI research)

**Frontend:**
- React + Vite (fast, modern)
- Axios (API calls)
- Clean, minimal UI

**Deployment:**
- Phase 1: Run locally on your laptop (4 participants)
- Phase 2: Deploy to Render.com (12 remote participants)

---

## Quick Start (10 minutes to running)

### 1. Backend Setup

```bash
cd peer-learning-platform/backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Run server
uvicorn main:app --reload --port 8000
```

Backend will be at: `http://localhost:8000`

### 2. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be at: `http://localhost:3000`

### 3. Test It Works

1. Open `http://localhost:3000` in browser
2. Enter your name → You'll be assigned participant ID
3. Platform guides you through entire 34-min session automatically

---

## How It Works (For CW3 Implementation Section)

### Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │  HTTP   │   FastAPI    │   API   │   GPT-4     │
│   Frontend  │ ──────> │   Backend    │ ──────> │   (OpenAI)  │
│             │         │              │         │             │
│  - Login    │         │ - Sessions   │         │ - Facilitate│
│  - Chat     │         │ - Bots       │         │ - Coach     │
│  - Quiz     │         │ - LLM calls  │         │             │
│  - Reflect  │         │ - Data log   │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   SQLite DB  │
                         │              │
                         │ - Messages   │
                         │ - Quizzes    │
                         │ - Preferences│
                         └──────────────┘
```

### Bot Behavior (Realistic Simulation)

**Based on HCI research findings:**
- Variable response delays: 45-90 seconds (randomized to avoid pattern detection)
- Behavior distribution:
  - 70% Affirmations ("That makes sense!", "Good point")
  - 20% Questions ("Can you explain that?", "What about...?")
  - 10% Contributions (topic-specific insights)
- Personality differences:
  - **Alex:** More questioning, hesitant ("hmm, I think maybe...")
  - **Jordan:** More confident, occasionally self-corrects ("Oh wait, actually...")
- Realistic imperfections:
  - Filler words ("wait", "interesting", "hmm")
  - Occasional mistakes that get corrected
  - Context-aware responses

### Session Flow (Automated)

**Module 1 (16 minutes):**
1. Platform Intro (1 min): Welcome, show Challenge Question
2. Info Priming (2-3 mins): Read conceptual explanation
3. Discussion (8-9 mins):
   - **LLM-Only:** LLM posts questions, synthesizes, encourages
   - **Rotating Anchor:** 3x3-minute rotations, participant facilitates for 3 mins with private coaching
4. Quiz (2 mins): 6 multiple-choice questions
5. Reflection (2 mins): Two open-ended prompts

**Rest (1 minute)**

**Module 2 (16 minutes):** Same structure, alternate condition & topic

**Final Choice (2 minutes):** Which format helped you learn more?

### Counterbalancing (Automatic Assignment)

Participants assigned round-robin to groups 1-4:

| Group | Module 1 Condition | Module 1 Topic | Module 2 Condition | Module 2 Topic |
|-------|-------------------|----------------|-------------------|----------------|
| 1     | LLM-Only         | Lazy/Eager     | Rotating Anchor   | Parallelism    |
| 2     | LLM-Only         | Parallelism    | Rotating Anchor   | Lazy/Eager     |
| 3     | Rotating Anchor  | Lazy/Eager     | LLM-Only          | Parallelism    |
| 4     | Rotating Anchor  | Parallelism    | LLM-Only          | Lazy/Eager     |

**P001 → Group 1, P002 → Group 2, P003 → Group 3, P004 → Group 4, P005 → Group 1...**

### Data Logging (Automatic)

**Everything is logged to SQLite database:**
- Participant info (ID, group, name, post-debrief consent)
- Session metadata (condition, topic, start/end times)
- All chat messages (timestamp, sender, content, public/private)
- Quiz responses (question, answer, correct/incorrect)
- Reflections (effectiveness text, helpful aspects)
- Final preferences (choice + explanation)

**Export for analysis:**
```bash
curl http://localhost:8000/api/data/export > study_data.json
```

---

## Running Your Study

### Phase 1: In-Person (4 Participants)

**Setup:**
1. Start backend & frontend on your laptop
2. Connect laptop to display/projector
3. Have WiFi available for participants to connect their devices

**Per Participant:**
```
1. Give them the URL: http://your-laptop-ip:3000
2. They enter their name
3. Platform auto-assigns them (P001-P004, one per group)
4. They complete 34-min session independently
5. You observe for technical issues only
```

**After Phase 1:**
- Review logs for any crashes
- Make minor fixes if needed (bug fixes only, no protocol changes)

### Phase 2: Remote (12 Participants)

**Deploy to cloud:**
```bash
# Option 1: Render.com (Easiest - Free Tier)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repo
4. Set build command: pip install -r requirements.txt
5. Set start command: uvicorn main:app --host 0.0.0.0 --port $PORT
6. Add environment variable: OPENAI_API_KEY
7. Deploy!

# Option 2: Heroku, Railway.app, etc. (similar process)
```

**Recruit participants:**
- Send them deployed URL
- They complete study on their own devices
- Monitor dashboard for crashes: http://your-url/api/data/export

**Monitoring (minimal):**
- Check logs occasionally for technical errors
- DON'T watch discussions in real-time (preserve autonomy)

---

## Troubleshooting

**Bot isn't responding:**
- Check backend logs - likely API rate limit or timeout
- Reduce `BOT_RESPONSE_DELAY_MIN/MAX` in config.py for testing

**Frontend can't connect to backend:**
- Ensure backend running on port 8000
- Check vite.config.js proxy settings
- CORS should allow localhost:3000

**Database errors:**
- Delete `peer_learning.db` to reset (WARNING: loses all data)
- Run backend again - tables recreate automatically

**GPT-4 API errors:**
- Check OpenAI API key in .env
- Verify API credits available
- Check quota limits

---

## For CW3 Report

### Implementation Section (15%)

**What to write:**

**Platform Architecture:**
- FastAPI backend for session orchestration and data logging
- React frontend for participant interface
- SQLite database for persistent storage
- GPT-4 API integration for LLM facilitation/coaching

**Bot Design:**
- Scripted finite state machine with 3 states: Affirm (70%), Question (20%), Contribute (10%)
- Variable response delays (45-90s) randomized per message
- Personality differentiation (Alex: tentative, Jordan: confident)
- Topic-specific contribution pools based on priming content
- Context-awareness: responds to questions, checks current anchor in Rotating condition

**LLM Integration:**
- **LLM-Only condition:** System prompt instructs GPT-4 to facilitate discussion (ask open questions, synthesize, encourage)
- **Rotating Anchor condition:** System prompt coaches current anchor with specific suggestions
- Temperature=0.7 for natural variation
- Max tokens limited (150 for facilitation, 80 for coaching) to keep responses concise

**Technical Challenges Solved:**
1. **Realistic bot timing:** Async task scheduling with random delays prevents pattern detection
2. **Counterbalancing automation:** Round-robin assignment ensures balanced groups
3. **Private messaging:** LLM coaching visible only to current anchor
4. **Session state management:** In-memory manager tracks current phase, anchor, discussion history
5. **Data integrity:** All messages timestamped, anonymized participant IDs (P001-P016)

### Results Section (30%)

**Data Analysis Plan:**

```python
# Primary Analysis: Paired t-test
import pandas as pd
from scipy.stats import ttest_rel

# Load quiz scores
df = pd.read_csv('quiz_scores.csv')

# Within-subjects comparison
llm_only_scores = df[df['condition'] == 'llm_only']['score_percentage']
rotating_anchor_scores = df[df['condition'] == 'rotating_anchor']['score_percentage']

t_stat, p_value = ttest_rel(llm_only_scores, rotating_anchor_scores)
effect_size = (rotating_anchor_scores.mean() - llm_only_scores.mean()) / rotating_anchor_scores.std()

print(f"Mean LLM-Only: {llm_only_scores.mean():.2f}%")
print(f"Mean Rotating Anchor: {rotating_anchor_scores.mean():.2f}%")
print(f"t({len(df)-1}) = {t_stat:.3f}, p = {p_value:.3f}")
print(f"Cohen's d = {effect_size:.3f}")
```

**Secondary Analysis: Preference proportions**
```python
# Condition preference
preferences = df['preferred_condition'].value_counts()
print(f"LLM-Only: {preferences.get('llm_only', 0)}/{len(df)}")
print(f"Rotating Anchor: {preferences.get('rotating_anchor', 0)}/{len(df)}")
print(f"Both Equal: {preferences.get('both_equal', 0)}/{len(df)}")

# Thematic coding of explanations (manual)
```

---

## Files Created

**Backend (Python):**
- `main.py` - FastAPI app with all endpoints
- `config.py` - Study settings & counterbalancing
- `database.py` - SQLite models (participants, sessions, messages, etc.)
- `bot_logic.py` - Realistic bot behavior
- `llm_service.py` - GPT-4 integration
- `content.py` - Priming texts, quizzes, challenge questions
- `requirements.txt` - Python dependencies

**Frontend (React):**
- `src/main.jsx` - Entry point
- `src/App.jsx` - Main application
- `src/components/` - Login, Chat, Quiz, Reflection, FinalChoice
- `vite.config.js` - Dev server config
- `package.json` - npm dependencies

**Docs:**
- This README
- `.env.example` - Environment variables template

---

## IMPORTANT: Before Running Study

1. **Ethics approval:** Ensure institutional review board approval
2. **Informed consent:** Use provided templates from CW2
3. **Debrief:** After session, explain AI bots, confirm post-debrief consent
4. **Data privacy:** Never share raw data with identifiable information

---

## Outstanding Work Tips

**For Implementation Section:**
1. Include architecture diagram (draw.io or similar)
2. Show actual GPT-4 prompts you used
3. Explain bot behavior patterns from research citations
4. Discuss technical challenges and solutions

**For Results Section:**
1. Report descriptive statistics FIRST (means, SDs, ranges)
2. Then inferential tests (paired t-test)
3. Include effect sizes (Cohen's d)
4. Show individual participant patterns (not just averages)
5. Report preference explanations thematically

**For Discussion Section:**
1. Compare to Cai et al.'s findings
2. Discuss unexpected patterns
3. Acknowledge limitations (12-min discussion, bot detection, etc.)
4. Suggest improvements for future work

---

## Support

**If something breaks:**
1. Check backend logs: Look at terminal running `uvicorn`
2. Check browser console: F12 in Chrome/Firefox
3. Export data frequently: Don't lose participant data!

**Questions about the code?**
- All files are heavily commented
- Architecture is modular - each file has one clear purpose
- Read the code - it's your best documentation

---

**Ready to run your study! Good luck with CW3!** 🎯
