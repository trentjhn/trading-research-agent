# 🚀 Push to GitHub

## Quick Commands to Push Everything

```bash
# Make sure you're in the project root
cd /Users/t-rawww/trading-agent

# Add all new files
git add .

# Commit with a descriptive message
git commit -m "Add beautiful web app with Next.js frontend and FastAPI backend"

# Push to your GitHub repo
git push origin main
```

If you get an error about the branch name, try:
```bash
git push origin master
```

---

## What Will Be Added

### Backend (FastAPI)
- `backend/main.py` - REST API with WebSocket support
- `backend/websocket_handler.py` - Real-time updates
- `backend/requirements.txt` - Python dependencies

### Frontend (Next.js)
- `frontend/app/` - Pages and layouts
- `frontend/components/` - React components
- `frontend/package.json` - Node dependencies
- All configuration files (tailwind, typescript, etc.)

### Documentation
- `WEB_APP_README.md` - Complete web app guide
- `INSTALL_WEBAPP.md` - Installation instructions
- `QUICKSTART.md` - Quick start guide
- `TROUBLESHOOTING.md` - Troubleshooting help

### Scripts
- `start-webapp.sh` - Start both servers
- `start-backend.sh` - Start backend only
- `start-frontend.sh` - Start frontend only
- `test-backend.sh` - Test backend API

---

## Before Pushing (Optional)

### Update .gitignore

Make sure these are in your `.gitignore`:

```bash
# Add to .gitignore if not already there
echo "
# Frontend
frontend/node_modules/
frontend/.next/
frontend/out/

# Python
__pycache__/
*.pyc
.env

# OS
.DS_Store
" >> .gitignore
```

### Check What Will Be Committed

```bash
git status
```

This shows all files that will be added.

---

## Step-by-Step Guide

1. **Check current status:**
   ```bash
   git status
   ```

2. **Add all new files:**
   ```bash
   git add backend/
   git add frontend/
   git add *.sh
   git add *.md
   ```

3. **Commit:**
   ```bash
   git commit -m "Add production-ready web app

   - FastAPI backend with REST and WebSocket APIs
   - Next.js 14 frontend with beautiful UI
   - Real-time stock analysis streaming
   - Comprehensive documentation
   - Simple startup scripts"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin main
   ```

---

## After Pushing

Your repo will have:
- ✅ Full web application
- ✅ Backend API
- ✅ Frontend UI
- ✅ Documentation
- ✅ Easy setup scripts

Others can clone and run:
```bash
git clone https://github.com/trentjhn/trading-research-agent.git
cd trading-research-agent

# Install dependencies
cd backend && pip3 install -r requirements.txt --user && cd ..
cd frontend && npm install && cd ..

# Run the app
./start-webapp.sh
```

---

## Troubleshooting

### "Nothing to commit"
You might have already committed some files. Check with:
```bash
git status
```

### "Permission denied"
Make sure you're authenticated with GitHub:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### "Remote rejected"
You might need to pull first:
```bash
git pull origin main --rebase
git push origin main
```

---

## Ready to Push?

Run these commands:

```bash
git add .
git commit -m "Add beautiful web app with Next.js frontend and FastAPI backend"
git push origin main
```

Then check your repo at: https://github.com/trentjhn/trading-research-agent

