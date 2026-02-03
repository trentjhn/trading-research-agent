# 🔧 Troubleshooting Guide

## Issue: "Website can't be reached"

This means the frontend isn't running yet. Here's how to fix it:

### Solution 1: Install Frontend Dependencies First

The frontend needs Node.js dependencies installed before it can run.

```bash
# Fix npm permissions (if needed)
sudo chown -R $(whoami) ~/.npm

# Install frontend dependencies
cd frontend
npm install
cd ..
```

This will take 2-3 minutes the first time.

### Solution 2: Test Backend Only (Faster)

While the frontend installs, you can test the backend API directly:

```bash
# Test the backend
./test-backend.sh
```

Then visit **http://localhost:8000/docs** to see the interactive API documentation!

### Solution 3: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
python3 main.py
```

**Terminal 2 - Frontend (after npm install completes):**
```bash
cd frontend
npm run dev
```

---

## Common Issues

### 1. Port 8000 Already in Use

```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Then restart
cd backend && python3 main.py
```

### 2. Port 3000 Already in Use

```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
cd frontend && PORT=3001 npm run dev
```

### 3. npm Permission Errors

```bash
# Fix npm cache permissions
sudo chown -R $(whoami) ~/.npm

# Then try again
cd frontend && npm install
```

### 4. "next: command not found"

This means npm dependencies aren't installed yet.

```bash
cd frontend
npm install
```

Wait for it to complete, then try again.

---

## Quick Test Checklist

✅ **Backend Working?**
```bash
curl http://localhost:8000/
```

Should return: `{"status":"online","service":"Trading Research Agent API","version":"1.0.0"}`

✅ **Frontend Dependencies Installed?**
```bash
ls frontend/node_modules
```

Should show many folders. If empty or doesn't exist, run `npm install` in the frontend directory.

✅ **Can Analyze a Stock?**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

Should return JSON with analysis data.

---

## What's Working Right Now

✅ **Backend** - Fully functional, dependencies installed  
✅ **CLI Agent** - Working perfectly (try `python3 -m src.main TSLA`)  
⏳ **Frontend** - Needs `npm install` to be run first

---

## Next Steps

1. **Install frontend dependencies:**
   ```bash
   cd frontend && npm install
   ```

2. **Start both servers:**
   ```bash
   ./start-webapp.sh
   ```

3. **Open browser:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

---

## Still Having Issues?

Try the backend-only test:
```bash
./test-backend.sh
```

This will confirm the backend is working while you troubleshoot the frontend.

