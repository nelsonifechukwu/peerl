# TROUBLESHOOTING GUIDE

**Common issues and solutions**

---

## Backend Won't Start

### Error: `ModuleNotFoundError: No module named 'fastapi'`

**Problem:** Dependencies not installed

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Error: `openai.error.AuthenticationError`

**Problem:** OpenAI API key missing or invalid

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check it has your key
cat .env

# Should show: OPENAI_API_KEY=sk-...

# If missing, create it:
echo "OPENAI_API_KEY=your-actual-key" > .env
```

### Error: `Address already in use`

**Problem:** Port 8000 already taken

**Solution:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

### Error: `sqlalchemy.exc.OperationalError`

**Problem:** Database corruption

**Solution:**
```bash
# Backup data first!
curl http://localhost:8000/api/data/export > backup.json

# Delete database
rm peer_learning.db

# Restart backend (it recreates tables)
uvicorn main:app --reload
```

---

## Frontend Won't Start

### Error: `Cannot find module 'react'`

**Problem:** Dependencies not installed

**Solution:**
```bash
cd frontend
npm install
```

### Error: `EADDRINUSE: address already in use`

**Problem:** Port 3000 already taken

**Solution:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or edit vite.config.js to use different port:
server: {
  port: 3001  // Change this
}
```

### Error: `Failed to fetch`

**Problem:** Frontend can't connect to backend

**Solution:**
1. Check backend is running: http://localhost:8000
2. Check CORS settings in backend/main.py:
```python
allow_origins=["http://localhost:3000"]  # Must match frontend URL
```

---

## Bot Issues

### Bots Never Respond

**Problem 1:** OpenAI API rate limit

**Solution:**
- Check OpenAI dashboard for rate limits
- Free tier: 3 requests/min
- Paid tier: Higher limits
- Space out bot responses more in config.py:
```python
BOT_RESPONSE_DELAY_MIN = 120  # Increase from 45
```

**Problem 2:** API error

**Solution:**
```bash
# Check backend logs for errors like:
# "OpenAI API Error: Rate limit exceeded"
# "OpenAI API Error: Insufficient quota"

# View logs in terminal running uvicorn
```

### Bots Respond Too Fast

**Problem:** Timing feels unnatural

**Solution:**
```python
# In backend/config.py, increase delays:
BOT_RESPONSE_DELAY_MIN = 60   # Was 45
BOT_RESPONSE_DELAY_MAX = 120  # Was 90
```

### Bots Say Weird Things

**Problem:** Bot behavior not matching topic

**Solution:**
```python
# Check backend/bot_logic.py
# Ensure topic-specific contributions are correct
# For lazy/eager topic, contributions should mention:
# - upfront cost vs ongoing cost
# - memory usage
# - access patterns
```

---

## LLM Issues

### LLM Facilitator Silent

**Problem:** LLM not generating responses

**Check:**
1. OpenAI API key valid
2. GPT-4 access enabled on your account
3. Sufficient credits

**Debug:**
```python
# In backend/llm_service.py, add print statements:
try:
    response = await openai.ChatCompletion.acreate(...)
    print(f"LLM Response: {response}")  # Add this
except Exception as e:
    print(f"LLM Error: {e}")  # Add this
```

### LLM Responses Too Long

**Problem:** LLM writing paragraphs instead of 1-2 sentences

**Solution:**
```python
# In backend/llm_service.py, reduce max_tokens:
response = await openai.ChatCompletion.acreate(
    model=OPENAI_MODEL,
    messages=messages,
    max_tokens=80,  # Reduce from 150
    temperature=0.7,
)
```

### LLM Goes Off-Topic

**Problem:** LLM discussing things unrelated to challenge question

**Solution:**
```python
# In backend/llm_service.py, strengthen system prompt:
system_prompt = f"""You are facilitating a learning discussion.
CRITICAL: Stay focused on the challenge question below.
Do not discuss other topics.
Keep responses to 1-2 sentences maximum.

Challenge Question:
{challenge_question}
"""
```

---

## Data Issues

### Quiz Scores All Wrong

**Problem:** Correct answers not matching actual correct answers

**Solution:**
```python
# Check backend/content.py
# For each quiz question, verify "correct" field:
{
    "id": 1,
    "question": "...",
    "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
    "correct": "A",  # <-- Must match actual correct answer!
}
```

### Data Not Saving

**Problem:** Database write failures

**Debug:**
```bash
# Check database permissions
ls -la peer_learning.db

# Should be writable by your user

# Check logs for SQLAlchemy errors
# Look for: "OperationalError" or "IntegrityError"
```

### Export Returns Empty Data

**Problem:** No participants showing up

**Solution:**
```bash
# Check if database file exists
ls -la peer_learning.db

# If missing, backend wasn't running when participants registered

# Check file size
ls -lh peer_learning.db

# If 0 bytes, data not being written
```

---

## Session Flow Issues

### Session Stuck on One Phase

**Problem:** Timer not advancing automatically

**Debug:**
```javascript
// In frontend/src/components/SessionFlow.jsx
// Check useEffect for phase transitions:

useEffect(() => {
  console.log(`Phase: ${phase}, Time: ${timeRemaining}`);  // Add this
  
  if (timeRemaining > 0) {
    const timer = setTimeout(() => {
      setTimeRemaining(time => time - 1)
    }, 1000)
    return () => clearTimeout(timer)
  } else {
    handlePhaseComplete()  // Should trigger here
  }
}, [timeRemaining, phase])
```

### Participant Can't Submit Quiz

**Problem:** Submit button disabled

**Solution:**
```javascript
// Check Quiz.jsx - button is disabled if not all questions answered
// Debug:
console.log(`Responses: ${Object.keys(responses).length}/${quiz.length}`)

// Make sure participant clicked all radio buttons
```

### Chat Messages Not Appearing

**Problem:** Messages sent but not showing

**Debug:**
```javascript
// In Chat.jsx, check polling:
useEffect(() => {
  const fetchMessages = async () => {
    try {
      const response = await axios.get(`/api/sessions/${sessionKey}/messages`)
      console.log(`Fetched ${response.data.length} messages`)  // Add this
      setMessages(response.data)
    } catch (error) {
      console.error('Error fetching messages:', error)
    }
  }
  
  fetchMessages()
  pollInterval.current = setInterval(fetchMessages, 2000)  // Poll every 2s
  
  return () => clearInterval(pollInterval.current)
}, [sessionKey])
```

---

## Deployment Issues

### Render: Build Fails

**Error:** `ERROR: Could not find a version that satisfies the requirement...`

**Solution:**
- Check requirements.txt has correct package names
- Pin versions: `fastapi==0.104.1` not just `fastapi`
- Ensure Python 3.9+ specified

### Render: App Crashes After Deploy

**Problem:** App starts locally but not on Render

**Debug:**
1. Check Render logs (Logs tab in dashboard)
2. Look for errors in startup
3. Common issues:
   - Missing environment variable: `OPENAI_API_KEY`
   - Wrong start command
   - Import errors (missing package in requirements.txt)

### CORS Errors in Production

**Error:** Browser console shows: `CORS policy: No 'Access-Control-Allow-Origin'`

**Solution:**
```python
# In backend/main.py, add your deployed URL:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-app.onrender.com"  # Add this!
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Lost After Redeploy

**Problem:** Render/Heroku reset filesystem on redeploy

**Solution:**
- This is expected behavior with free tiers
- Export data frequently:
```bash
curl https://your-app.onrender.com/api/data/export > backup_$(date +%Y%m%d).json
```
- For production, consider:
  - PostgreSQL addon (Render/Heroku)
  - Or accept SQLite resets and export daily

---

## Performance Issues

### Backend Slow to Respond

**Problem:** Requests taking >5 seconds

**Possible Causes:**
1. **OpenAI API slow:** First call can take 3-5 seconds
2. **Free tier sleeping:** Render free tier sleeps after inactivity
3. **Too many bots responding:** Reduce bot response probability

**Solutions:**
```python
# Reduce bot chatter in config.py:
BOT_AFFIRMATION_PROB = 0.50  # Was 0.70
BOT_QUESTION_PROB = 0.15     # Was 0.20

# Increase response delays:
BOT_RESPONSE_DELAY_MIN = 90  # Was 45
```

### Frontend Laggy

**Problem:** UI feels slow or unresponsive

**Solution:**
```javascript
// Reduce polling frequency in Chat.jsx:
pollInterval.current = setInterval(fetchMessages, 5000)  // Was 2000 (5s instead of 2s)
```

---

## Participant Experience Issues

### "I think Alex/Jordan is a bot"

**Problem:** Participant detected bots

**This is OK!**
- Some participants will detect bots (~60%)
- This is noted in your methodology
- Proceed normally, don't confirm/deny during session
- Reveal in debrief as planned
- Ask in post-study questionnaire: "Did you suspect bots?"

### Participant Confused About Role

**Problem:** "Am I supposed to facilitate?"

**Solution:**
- Improve instructions in SessionFlow.jsx:
```javascript
{sessionData.condition === 'rotating_anchor' && (
  <div className="info-box">
    <p><strong>In this session:</strong></p>
    <p>You'll take turns facilitating the discussion.</p>
    <p>When it's your turn, you'll receive coaching suggestions.</p>
    <p>When it's someone else's turn, contribute as a participant.</p>
  </div>
)}
```

### Participant Rushes Through

**Problem:** Completes in 20 minutes instead of 34

**Possible Reasons:**
- Didn't read priming text carefully
- Didn't engage in discussion
- Rushed quiz

**Solution:**
- Add warnings:
```javascript
// In priming phase:
<p style={{ color: 'red', fontWeight: 'bold' }}>
  Please read carefully. You'll need this information for the discussion.
</p>
```

---

## Browser Compatibility

### Works in Chrome, Breaks in Safari

**Common Issues:**
- Fetch API polyfill needed
- Async/await support
- CSS grid issues

**Solution:**
```bash
# Add polyfills to frontend:
npm install --save-dev @vitejs/plugin-legacy
```

### Mobile Display Issues

**Problem:** Layout broken on phones

**Solution:**
```css
/* In index.css, add mobile-specific rules: */
@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  .chat-container {
    height: 300px;  /* Shorter on mobile */
  }
  
  .timer {
    position: static;  /* Don't float on mobile */
    margin-bottom: 20px;
  }
}
```

---

## Emergency Procedures

### Complete System Failure During Study

**If everything crashes:**
1. **DON'T PANIC**
2. Export any available data immediately
3. Note exactly what broke and when
4. Contact affected participants:
   - Apologize
   - Explain technical issue
   - Offer to reschedule
   - Offer compensation if appropriate
5. Fix issue, test thoroughly
6. Resume study

### Data Corruption

**If database corrupted:**
1. Don't delete anything!
2. Try SQLite recovery:
```bash
sqlite3 peer_learning.db ".recover" > recovered.sql
sqlite3 new_database.db < recovered.sql
```
3. Contact participants if data lost
4. Document in CW3 limitations

### Participant Withdraws Data

**If participant withdraws consent:**
1. Thank them for participating
2. Delete their data immediately:
```sql
DELETE FROM participants WHERE id = 'P007';
-- This cascades to all related data
```
3. Document withdrawal (not why)
4. Recruit replacement if needed

---

## Getting Help

**Still stuck?**

1. **Check Logs:**
   - Backend: Terminal running uvicorn
   - Frontend: Browser console (F12)
   - Deployed: Platform dashboard logs

2. **Search Error Messages:**
   - Copy exact error
   - Google: "FastAPI [error message]"
   - Check Stack Overflow

3. **Test in Isolation:**
   - Does backend work alone? `curl http://localhost:8000/`
   - Does frontend work alone? Check browser console
   - Do they connect? Check network tab in browser

4. **Start Fresh:**
   ```bash
   # Nuclear option - clean slate
   rm -rf backend/peer_learning.db
   rm -rf frontend/node_modules
   cd frontend && npm install
   cd ../backend && pip install -r requirements.txt
   # Start both servers
   ```

5. **Read the Code:**
   - All files heavily commented
   - Follow execution flow
   - Add print statements to debug

---

**Remember: Most issues are simple:**
- Missing dependency
- Wrong URL/port
- API key not set
- CORS misconfigured

**Check these first before deeper debugging!**
