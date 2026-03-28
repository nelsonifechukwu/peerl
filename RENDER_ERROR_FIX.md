# RENDER DEPLOYMENT ERROR FIX

**Error:** `pydantic-core` build failure on Render
**Cause:** Python 3.14 too new, no pre-built wheels available
**Status:** ✅ FIXED

---

## THE ERROR YOU SAW

```
error: failed to create directory `/usr/local/cargo/registry/cache/...`
Caused by: Read-only file system (os error 30)
💥 maturin failed
Error running maturin: Command '['maturin', 'pep517', 'write-dist-info'...
```

---

## WHY IT HAPPENED

1. **Render defaults to Python 3.14** (latest version)
2. **pydantic-core needs to compile** (Rust-based package)
3. **No pre-built wheels for Python 3.14 yet**
4. **Build tries to compile from source → fails**

---

## THE FIX (3 FILES UPDATED)

### ✅ 1. runtime.txt (NEW FILE)
```
python-3.11.9
```
**Purpose:** Tells Render to use Python 3.11.9 (stable, has pre-built wheels)

### ✅ 2. requirements.txt (UPDATED)
```
pydantic==2.4.2
pydantic-core==2.10.1
```
**Purpose:** Pin to versions with guaranteed pre-built wheels

### ✅ 3. render.yaml (UPDATED)
Added Python version specification

---

## HOW TO DEPLOY NOW

### Option A: Automatic (if you have runtime.txt in root)

Render will automatically detect `runtime.txt` and use Python 3.11.9

### Option B: Manual (set in Render dashboard)

1. Go to Render dashboard
2. Select your backend service
3. **Environment** tab
4. Add: `PYTHON_VERSION = 3.11.9`
5. **Redeploy**

---

## STEP-BY-STEP DEPLOYMENT

### 1. Push Updated Code to GitHub

```bash
cd peer-learning-platform/backend

# Make sure you have the updated files:
ls runtime.txt         # Should exist now
cat requirements.txt   # Should show pydantic==2.4.2

# Commit and push
git add .
git commit -m "Fix Render deployment - pin Python 3.11.9"
git push
```

### 2. Deploy on Render

**First Time:**
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. **Root Directory:** `backend`
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. **Environment Variables:**
   - `OPENAI_API_KEY = your-key-here`
8. **Create Web Service**

**Already Deployed:**
1. Go to your service dashboard
2. **Manual Deploy** → **Deploy latest commit**
3. Watch logs - should work now!

---

## VERIFY IT WORKED

**Check Render logs, should see:**

```
==> Downloading buildpack...
==> Python version set to 3.11.9
==> Installing dependencies...
    Collecting fastapi==0.104.1
    Collecting pydantic==2.4.2
      Downloading pydantic-2.4.2-py3-none-any.whl (395 kB)  ✅ Pre-built wheel!
    Collecting pydantic_core==2.10.1
      Downloading pydantic_core-2.10.1-cp311-cp311-manylinux_2_17_x86_64.whl ✅ Pre-built!
==> Build succeeded!
```

**Key indicators:**
- ✅ "Python version set to 3.11.9"
- ✅ "Downloading pydantic_core...whl" (not building from source)
- ✅ "Build succeeded!"

---

## TEST YOUR DEPLOYED BACKEND

```bash
# Health check
curl https://your-backend.onrender.com/

# Should return:
{"status":"Peer Learning Platform API Running"}
```

---

## ALTERNATIVE FIX (If Above Doesn't Work)

### Use Python 3.12 Instead

**runtime.txt:**
```
python-3.12.7
```

**Why:** Python 3.12 also has good wheel support and is stable.

---

## COMMON DEPLOYMENT ERRORS

### Error: "No module named 'dotenv'"
**Fix:** Already in requirements.txt as `python-dotenv`

### Error: "No module named 'uvicorn'"
**Fix:** Already in requirements.txt

### Error: "OPENAI_API_KEY not found"
**Fix:** Add environment variable in Render dashboard

### Error: CORS issues
**Fix:** Update `allow_origins` in main.py:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-frontend.onrender.com"  # Add this!
]
```

---

## FILES YOU NEED

Make sure you have these 3 files in `backend/`:

1. ✅ **runtime.txt** - Python version
2. ✅ **requirements.txt** - Updated dependencies  
3. ✅ **render.yaml** - Deployment config

All are included in the updated download!

---

## SUMMARY

**Problem:** Python 3.14 too new, pydantic-core can't build
**Solution:** Pin to Python 3.11.9 with runtime.txt
**Result:** Uses pre-built wheels, builds successfully

---

## NEXT STEPS

1. Re-download the platform (has all fixes)
2. Push to GitHub
3. Deploy to Render
4. Should work now! ✅

---

**If you still get errors, check:**
- runtime.txt exists in backend/
- Python version shows 3.11.9 in Render logs
- requirements.txt has pydantic==2.4.2

**All fixed files ready in /mnt/user-data/outputs/** 🚀
