# ✅ DO THIS NOW - Merge Frontend + Backend

## Your Branches

I can see you have:
- ✅ `backend` (current - your work)
- ✅ `frontend` (your frontend)
- ✅ `development` (possibly has other features)
- ✅ `feature/voice-accessibility` (voice features)

## Step-by-Step Merge Instructions

### Step 1: Commit Current Backend Work (1 minute)

```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK

# Check what's not committed
git status

# Add everything
git add .

# Commit with clear message
git commit -m "feat: complete backend with Azure Search, Blob Storage, and 9 AI tools"

# Push to backend branch
git push origin backend
```

### Step 2: Merge Frontend (2 minutes)

```bash
# Make sure you're on backend branch
git checkout backend

# Fetch all latest changes from remote
git fetch origin

# Merge frontend branch into backend
git merge origin/frontend --no-ff -m "merge: integrate frontend with backend"
```

**Expected outcome:**
- Git might auto-merge if no conflicts
- Or it will show conflicts to resolve

### Step 3: If You Get Conflicts (Skip if no conflicts)

Git will show something like:
```
CONFLICT (content): Merge conflict in .env
CONFLICT (content): Merge conflict in README.md
```

**To resolve:**

```bash
# See which files have conflicts
git status

# Open each conflicted file and:
# 1. Look for <<<<<<< HEAD
# 2. Choose what to keep
# 3. Remove conflict markers
# 4. Save file

# Common conflicts and how to handle:
```

**`.env` conflict - Keep both:**
```env
# Backend variables (keep these)
FOUNDRY_PROJECT_ENDPOINT=https://sahayak-christinhack.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.4-mini
AZURE_SEARCH_ENDPOINT=https://sahayak-search.search.windows.net
AZURE_SEARCH_KEY=...
AZURE_STORAGE_BLOB_CONNECTION_STRING=...
AZURE_STORAGE_CONTAINER_NAME=sahayak-knowledge

# Frontend variables (add these if they exist)
VITE_API_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**`.gitignore` conflict - Keep both:**
```
# Backend
__pycache__/
*.pyc
*.pyo
.env
*.log

# Frontend
node_modules/
dist/
build/
.next/
.nuxt/
```

**After resolving conflicts:**
```bash
git add .
git commit -m "merge: resolve conflicts and integrate frontend"
```

### Step 4: Merge Other Features (Optional)

If you want voice accessibility and development features:

```bash
# Merge development branch
git merge origin/development --no-ff -m "merge: add development features"

# Merge voice accessibility
git merge origin/feature/voice-accessibility --no-ff -m "merge: add voice accessibility feature"
```

### Step 5: Push Everything

```bash
git push origin backend
```

### Step 6: Check Your Project Structure

```bash
# See what's in your project now
ls -la

# You should see:
# - backend/ (your backend code)
# - frontend/ or src/ (your frontend code)
# - other folders from merged branches
```

## Quick Test After Merge

### Terminal 1 - Backend:
```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK
python backend/main.py
```

Should start on: `http://localhost:8000`

### Terminal 2 - Frontend:
```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK

# Find your frontend folder (it might be named differently)
# Could be: frontend/, client/, ui/, app/, src/

cd frontend  # or wherever your frontend is

# Install dependencies (if needed)
npm install  # or yarn install or pnpm install

# Start frontend
npm run dev  # or yarn dev or npm start
```

Should start on: `http://localhost:3000` (or 5173, 8080 depending on framework)

## Expected Project Structure After Merge

```
SAHAYAK/
├── backend/                 # ✅ Your backend
│   ├── main.py
│   ├── services/
│   │   ├── azure_search.py
│   │   └── blob_storage.py
│   ├── tools/
│   ├── routers/
│   └── requirements.txt
├── frontend/                # ✅ Your frontend (merged)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── .env                     # ✅ Combined env vars
├── .gitignore              # ✅ Combined rules
├── README.md
└── ...
```

## If Frontend Can't Connect to Backend

Add CORS to `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

# After: app = FastAPI(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then restart backend:
```bash
pkill -f "python.*main.py"
python backend/main.py
```

## Connect Frontend to Backend

Update your frontend API configuration:

**React/Vite - `.env` or `.env.local`:**
```env
VITE_API_URL=http://localhost:8000
```

**Next.js - `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**In your frontend code:**
```javascript
// API calls should go to
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';

// Example:
fetch(`${API_URL}/api/v1/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userMessage,
    session_id: sessionId
  })
})
```

## Backend API Endpoints Available

Your frontend can now use:

```javascript
// 1. Health check
GET http://localhost:8000/health

// 2. Chat with AI
POST http://localhost:8000/api/v1/chat
Body: { "message": "Hello", "session_id": "user_123" }

// 3. Search schemes (if you add this endpoint)
GET http://localhost:8000/api/v1/schemes?query=disability

// 4. Get scheme details
GET http://localhost:8000/api/v1/schemes/{scheme_id}

// 5. Check eligibility
POST http://localhost:8000/api/v1/eligibility/check
Body: { "user_profile": {...}, "scheme_id": "..." }

// 6. Get required documents
GET http://localhost:8000/api/v1/schemes/{scheme_id}/documents

// 7. API documentation
GET http://localhost:8000/docs
```

## Summary Commands (Copy-Paste)

```bash
# 1. Commit current work
git add .
git commit -m "feat: complete backend integration"
git push origin backend

# 2. Merge frontend
git merge origin/frontend --no-ff -m "merge: integrate frontend"

# 3. If conflicts, resolve and commit
git add .
git commit -m "merge: resolve conflicts"

# 4. Push
git push origin backend

# 5. Test
python backend/main.py  # Terminal 1
cd frontend && npm run dev  # Terminal 2
```

## Next Steps

After merge:
1. ✅ Both backend and frontend in same repo
2. ✅ Backend provides API at port 8000
3. ✅ Frontend connects to backend
4. ✅ Full stack application ready!

Need help with any step? Just ask! 🚀
