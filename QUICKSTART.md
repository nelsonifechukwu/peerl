# QUICK START GUIDE

**Get your platform running in 10 minutes!**

---

## Prerequisites

- Python 3.9+ installed
- Node.js 16+ installed
- OpenAI API key with GPT-4 access

---

## Setup

### 1. Backend (Terminal 1)

```bash
cd peer-learning-platform/backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your-actual-key-here" > .env

# Run server
uvicorn main:app --reload --port 8000
```

**Backend running at:** http://localhost:8000

### 2. Frontend (Terminal 2)

```bash
cd peer-learning-platform/frontend

# Install npm dependencies
npm install

# Run development server
npm run dev
```

**Frontend running at:** http://localhost:3000

---

## Test It Works

1. Open http://localhost:3000
2. Enter your name (e.g., "Test Participant")
3. You'll be assigned ID: P001
4. Platform guides you through entire 34-minute session

---

## What Happens

**Module 1 (16 mins):**
- Welcome screen → Read priming text → 
- Discuss with Alex & Jordan (AI bots) →
- Quiz → Reflection

**Rest (1 min)**

**Module 2 (16 mins):**
- Same structure, different topic & condition

**Final Choice (2 mins):**
- Pick which format helped you learn more

**Debrief:**
- Reveals bots, confirms consent

---

## Data Export

```bash
curl http://localhost:8000/api/data/export > study_data.json
```

All participant data, messages, quiz scores, preferences exported as JSON.

---

## Troubleshooting

**Backend won't start:**
- Check: Python 3.9+ installed
- Check: `.env` file exists with valid API key
- Try: Delete `peer_learning.db` and restart

**Frontend won't start:**
- Check: Node.js 16+ installed
- Try: Delete `node_modules` folder, run `npm install` again

**Bots not responding:**
- Check: Backend logs for API errors
- Check: OpenAI API has credits
- Check: No rate limits hit

**Can't connect to backend:**
- Ensure backend running on port 8000
- Check: http://localhost:8000 shows "API Running"

---

## Deploy for Remote Participants (Phase 2)

**Render.com (Easiest):**

1. Push code to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variable: `OPENAI_API_KEY=your-key`
5. Deploy!

**Your URL:** `https://your-app-name.onrender.com`

Send this to remote participants.

---

## File Structure

```
peer-learning-platform/
├── backend/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Study settings
│   ├── database.py       # Data models
│   ├── bot_logic.py      # Bot behavior
│   ├── llm_service.py    # GPT-4 integration
│   ├── content.py        # Topics & quizzes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main app
│   │   ├── components/   # All UI components
│   │   └── index.css     # Styling
│   └── package.json
└── README.md             # Full documentation
```

---

## Next Steps

1. **Test locally** with 2-3 people
2. **Run Phase 1** (4 in-person participants)
3. **Deploy to cloud** (Render.com)
4. **Run Phase 2** (12 remote participants)
5. **Export data** for analysis
6. **Write CW3** using README guidance

---

**Read README.md for complete details on:**
- Architecture explanation
- Bot behavior patterns
- Data analysis examples
- CW3 writing tips

**Good luck!** 🚀
