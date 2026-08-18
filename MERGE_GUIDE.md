# 🔄 Frontend + Backend Integration Guide

## Current Situation

- ✅ **Backend branch**: Has Azure Search, Blob Storage, all tools integrated
- ✅ **Frontend branch**: Has your UI and other features
- 🎯 **Goal**: Merge them together

## Step 1: Check Your Branches

```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK

# See all branches
git branch -a
```

## Step 2: Save Your Current Backend Work

Before merging, let's make sure all backend changes are committed:

```bash
# Check what's not committed
git status

# Add all backend changes
git add .

# Commit
git commit -m "feat: complete backend with Azure Search and Blob Storage integration"

# Push to backend branch
git push origin backend
```

## Step 3: Identify Your Frontend Branch

Common branch names:
- `frontend`
- `main`
- `development`
- `feature/frontend`

Let me check what you have:

```bash
# List all branches (local and remote)
git branch -a
```

## Step 4: Merge Frontend into Backend

### Option A: Merge Frontend Branch into Backend (Recommended)

If your frontend is in a separate branch (e.g., `frontend`):

```bash
# Make sure you're on backend branch
git checkout backend

# Fetch latest changes
git fetch origin

# Merge frontend branch into backend
git merge origin/frontend --no-ff

# Or if it's called main:
# git merge origin/main --no-ff
```

### Option B: Merge Main into Backend

If frontend is in `main`:

```bash
git checkout backend
git fetch origin
git merge origin/main --no-ff
```

## Step 5: Resolve Conflicts (If Any)

If you get merge conflicts:

```bash
# Git will show which files conflict
# Common conflicts:
# - README.md
# - .env
# - package.json (if both have it)
# - .gitignore
```

### How to Resolve:

1. **Open conflicted files** (Git marks them with `<<<<<<<`, `=======`, `>>>>>>>`)

2. **For each conflict:**
   - Keep backend version? Delete frontend lines
   - Keep frontend version? Delete backend lines
   - Keep both? Merge them manually

3. **Common files to handle:**

   **`.env` - Keep both, merge them:**
   ```env
   # Backend variables
   FOUNDRY_PROJECT_ENDPOINT=...
   AZURE_SEARCH_ENDPOINT=...
   AZURE_STORAGE_...=...
   
   # Frontend variables (if any)
   VITE_API_URL=http://localhost:8000
   REACT_APP_API_URL=http://localhost:8000
   ```

   **`.gitignore` - Merge both:**
   ```
   # Backend
   __pycache__/
   *.pyc
   .env
   
   # Frontend
   node_modules/
   dist/
   build/
   .next/
   ```

   **`README.md` - Keep both or write new one**

4. **After resolving:**
   ```bash
   # Mark as resolved
   git add .
   
   # Complete the merge
   git commit -m "merge: integrate frontend with backend"
   ```

## Step 6: Project Structure After Merge

Your project should look like:

```
SAHAYAK/
├── backend/                    # Your backend (current)
│   ├── main.py
│   ├── services/
│   │   ├── azure_search.py
│   │   └── blob_storage.py
│   ├── tools/
│   ├── routers/
│   └── ...
├── frontend/                   # Your frontend (from merge)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── .env                        # Merged environment variables
├── .gitignore                  # Merged ignore rules
└── README.md                   # Combined documentation
```

## Step 7: Update Frontend API Endpoint

After merging, update your frontend to point to the backend:

### If Using React/Vite:

**`.env` (in root):**
```env
VITE_API_URL=http://localhost:8000
```

**Frontend code:**
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Make API calls
fetch(`${API_URL}/api/v1/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Hello',
    session_id: 'user_123'
  })
})
```

### If Using Next.js:

**`.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Code:**
```javascript
const API_URL = process.env.NEXT_PUBLIC_API_URL;
```

## Step 8: Test the Integration

### Terminal 1 - Start Backend:
```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK
python backend/main.py
```

### Terminal 2 - Start Frontend:
```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK/frontend
npm install  # or yarn install
npm run dev  # or yarn dev
```

### Test:
1. Open browser: `http://localhost:3000` (or your frontend port)
2. Try interacting with the UI
3. Check if API calls work

## Step 9: Fix CORS (If Frontend Can't Connect)

If frontend shows CORS errors, update `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(...)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vue default
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 10: Create Unified Startup

**`start.sh` (for development):**
```bash
#!/bin/bash

# Start backend
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK
python backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"

# Wait for Ctrl+C
wait
```

Make it executable:
```bash
chmod +x start.sh
./start.sh
```

## Common Merge Scenarios

### Scenario 1: Frontend is in `main`, Backend in `backend`

```bash
git checkout backend
git merge origin/main --no-ff
# Resolve conflicts
git commit -m "merge: integrate frontend from main"
git push origin backend
```

### Scenario 2: Frontend is in `frontend` branch

```bash
git checkout backend
git merge origin/frontend --no-ff
# Resolve conflicts
git commit -m "merge: integrate frontend branch"
git push origin backend
```

### Scenario 3: Multiple Feature Branches

```bash
# Merge each feature branch one by one
git checkout backend
git merge origin/feature1 --no-ff
git merge origin/feature2 --no-ff
# etc.
```

## Quick Command Reference

```bash
# 1. Save current work
git add .
git commit -m "feat: backend integration complete"
git push origin backend

# 2. Check branches
git branch -a

# 3. Merge (replace 'frontend' with your branch name)
git checkout backend
git merge origin/frontend --no-ff

# 4. If conflicts, resolve and:
git add .
git commit -m "merge: integrate frontend"

# 5. Push merged result
git push origin backend

# 6. Test both
python backend/main.py  # Terminal 1
cd frontend && npm run dev  # Terminal 2
```

## Troubleshooting

### "Merge conflict in..."
- Open the file
- Look for `<<<<<<<`, `=======`, `>>>>>>>`
- Choose what to keep
- Remove conflict markers
- `git add <file>` and `git commit`

### "Already up to date"
- Your branch already has those changes
- No merge needed!

### "CONFLICT (content): Merge conflict in .env"
- Keep both sets of variables
- Backend vars + Frontend vars
- Don't duplicate anything

### Frontend can't connect to backend
1. Check CORS settings in `backend/main.py`
2. Check API URL in frontend
3. Make sure backend is running

## Next Steps After Merge

1. ✅ **Test backend**: `curl http://localhost:8000/health`
2. ✅ **Test frontend**: Open in browser
3. ✅ **Test integration**: Use frontend to call backend
4. ✅ **Update README**: Document the full stack
5. ✅ **Commit everything**: `git add . && git commit -m "chore: complete integration"`

## Need Help?

If you run into issues:
1. Show me the output of `git branch -a`
2. Show me any merge conflicts
3. Show me your project structure after merge

Let's do this! 🚀
