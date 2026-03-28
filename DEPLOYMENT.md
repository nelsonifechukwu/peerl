# DEPLOYMENT GUIDE - Phase 2 Remote Participants

**Deploy your platform to the cloud so remote participants can access it**

---

## Option 1: Render.com (RECOMMENDED - Easiest)

**Why Render:**
- Free tier available
- Simple setup (5 minutes)
- Automatic HTTPS
- Good for N=16 participants

### Step-by-Step:

**1. Prepare Your Code**

```bash
# Create a GitHub repository if you haven't already
cd peer-learning-platform
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub and push
# Follow GitHub instructions to add remote and push
```

**2. Deploy to Render**

1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your repository: `peer-learning-platform`
5. Configure:
   - **Name:** `peer-learning-study` (or whatever you want)
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

6. Add Environment Variable:
   - Click "Advanced" → "Add Environment Variable"
   - **Key:** `OPENAI_API_KEY`
   - **Value:** Your OpenAI API key

7. Click "Create Web Service"

**3. Wait for Deployment (2-3 minutes)**

Render will:
- Pull your code
- Install dependencies
- Start your server
- Give you a URL like: `https://peer-learning-study.onrender.com`

**4. Test Your Deployment**

```bash
# Check health
curl https://your-app-name.onrender.com/

# Should return: {"status":"Peer Learning Platform API Running"}
```

**5. Update Frontend**

Your frontend needs to talk to the deployed backend:

```javascript
// In frontend/vite.config.js, update proxy OR
// In frontend/src/components/*.jsx, replace '/api/' with full URL:

// Before:
const response = await axios.post('/api/participants', ...)

// After:
const response = await axios.post('https://your-app-name.onrender.com/api/participants', ...)
```

**Better approach:** Deploy frontend too!

1. In Render, create another Web Service
2. Select same repo
3. Configure:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm run preview`
   - **Environment Variable:** `VITE_API_URL=https://your-backend.onrender.com`

Now your frontend URL is: `https://your-frontend.onrender.com`

**6. Send to Participants**

Email participants the frontend URL:
```
Hello!

You're invited to participate in a collaborative learning study.

Study URL: https://your-frontend.onrender.com
Time commitment: 34 minutes
What you'll do: Discuss conceptual topics with other participants

Please complete by [deadline].

If you have questions, contact [your email].

Thank you!
```

---

## Option 2: Heroku

**1. Install Heroku CLI**
```bash
brew install heroku/brew/heroku  # Mac
# or download from https://devcenter.heroku.com/articles/heroku-cli
```

**2. Create Heroku App**
```bash
cd peer-learning-platform/backend
heroku login
heroku create peer-learning-study

# Add Python buildpack
heroku buildpacks:set heroku/python

# Set environment variable
heroku config:set OPENAI_API_KEY=your-key-here
```

**3. Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

**4. Open App**
```bash
heroku open
```

---

## Option 3: Railway.app

**1. Sign up at https://railway.app**

**2. New Project → Deploy from GitHub**

**3. Select repo, configure:**
- **Root Directory:** `backend`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables:** Add `OPENAI_API_KEY`

**4. Deploy!**

---

## Monitoring Your Deployed App

### Check Logs (Render)
1. Go to your service dashboard
2. Click "Logs" tab
3. Watch for errors in real-time

### Export Data Remotely
```bash
# From your laptop
curl https://your-app-name.onrender.com/api/data/export > study_data.json
```

### Check Participant Progress
```bash
# Count how many participants so far
curl https://your-app-name.onrender.com/api/data/export | \
  python -c "import sys, json; data=json.load(sys.stdin); print(f'Participants: {len(data[\"participants\"])}')"
```

---

## Troubleshooting Deployment

**App won't start:**
- Check logs for error messages
- Verify `OPENAI_API_KEY` is set correctly
- Ensure requirements.txt has all dependencies

**Database errors:**
- SQLite works on Render/Heroku (file-based)
- Database resets if app redeploys (export data frequently!)

**CORS errors (frontend can't connect):**
```python
# In backend/main.py, add your frontend URL to allow_origins:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.onrender.com"  # Add this
    ],
    ...
)
```

**Slow response times:**
- Free tier may sleep after inactivity
- First request wakes it up (30 seconds)
- Tell participants to be patient on first load

**API rate limits:**
- OpenAI has rate limits (3 requests/min on free tier)
- Upgrade to paid tier if needed
- Or space out participants (don't run 16 simultaneously)

---

## Best Practices

**1. Export data daily**
```bash
# Set up a cron job or run manually
curl https://your-app.onrender.com/api/data/export > backup_$(date +%Y%m%d).json
```

**2. Monitor participant flow**
- Check logs for errors
- Verify data is saving correctly
- Don't watch sessions in real-time (preserve autonomy)

**3. Test before sending to participants**
- Complete full 34-min session yourself
- Test on mobile device
- Test on different browsers
- Verify data exports correctly

**4. Shut down after study complete**
- Download all data
- Delete deployment (to avoid charges if you upgraded)
- Keep code in GitHub for CW3 reference

---

## Cost Estimate

**Free tier is sufficient for your study:**
- Render.com Free: 750 hours/month (enough for N=16)
- Heroku Free: 550 hours/month (enough)
- Railway Free: $5 credit (enough)

**If you need more reliability:**
- Render Starter: $7/month
- Heroku Hobby: $7/month
- Railway Pro: $5/month

**For N=16 participants × 34 minutes each:**
- Total compute time: ~9 hours
- Well within free tier limits

---

## Security Checklist

- [ ] `.env` file NOT committed to GitHub
- [ ] Environment variables set in deployment platform
- [ ] CORS configured correctly
- [ ] No sensitive data in frontend code
- [ ] Database backed up regularly
- [ ] Participant data anonymized (P001-P016)

---

## After Deployment

**Send this to participants:**

```
Subject: Collaborative Learning Study - Participate Now

Hello,

You're invited to participate in a research study on collaborative learning formats.

STUDY DETAILS:
- URL: [your-frontend-url]
- Time: 34 minutes
- What: Discuss educational topics with other participants
- Deadline: [date]

WHAT TO EXPECT:
1. Enter your name to begin
2. Read brief educational content
3. Discuss topics with peers
4. Answer short quizzes
5. Reflect on your experience

All participation is anonymous (you'll be assigned ID: P001, P002, etc.)

BEFORE YOU START:
- Find a quiet place with good internet
- Use Chrome, Firefox, or Safari (latest version)
- Don't refresh the page during the session

Questions? Contact: [your email]

Thank you for participating!

[Your name]
[Your institution]
```

---

## Emergency Procedures

**If app crashes during a session:**
1. Check logs immediately
2. Fix error
3. Redeploy
4. Contact affected participant
5. Offer to reschedule

**If database corrupts:**
1. Restore from latest backup
2. Contact participants who completed after backup
3. Ask if they're willing to redo (with compensation if needed)

**If you hit rate limits:**
1. Upgrade OpenAI tier temporarily
2. Or space out participants more

---

**You're ready to deploy! Choose Render.com for simplest setup.**
