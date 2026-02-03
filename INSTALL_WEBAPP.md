# 🚀 Web App Installation Guide

Quick guide to get your Trading Research Agent web app up and running!

## ✅ Prerequisites Check

Before starting, make sure you have:

- [x] Python 3.9+ installed
- [x] Node.js 18+ installed  
- [x] Anthropic API key (already in `.env`)

Check your versions:
```bash
python3 --version  # Should be 3.9+
node --version     # Should be 18+
```

## 📦 Installation

### Step 1: Install Dependencies (First Time Only)

**Backend:**
```bash
cd backend
pip3 install -r requirements.txt --user
cd ..
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### Step 2: Start the App

**Option A: Start Everything (Recommended)**
```bash
./start-webapp.sh
```

**Option B: Start Separately**

Terminal 1:
```bash
./start-backend.sh
```

Terminal 2:
```bash
./start-frontend.sh
```

That's it! Open `http://localhost:3000` 🎉

## 🎯 Using the App

1. **Open your browser** to `http://localhost:3000`

2. **Enter a stock ticker** (e.g., AAPL, TSLA, MSFT, NVDA)

3. **Click "Analyze"** and wait ~10 seconds

4. **View your report** with 5 tabs:
   - **Final Report**: AI-synthesized recommendation
   - **Fundamental**: Financial analysis
   - **Technical**: Price trends and indicators
   - **Sentiment**: News and market perception
   - **Macro**: Economic context

5. **Click "New Search"** to analyze another stock

## 🎨 What You'll See

### Landing Page
- Beautiful gradient hero section
- Search bar with ticker input
- 4 feature cards explaining analysis types
- Responsive design (works on mobile!)

### Analysis View
- Real-time loading animation
- Tabbed interface for different analyses
- Markdown-formatted reports
- Professional styling with dark mode support

## 🔧 Troubleshooting

### "Module not found" errors (Backend)
```bash
cd backend
pip3 install -r requirements.txt --user
```

### "Cannot find module" errors (Frontend)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
If port 8000 or 3000 is already in use:

**Backend (change port):**
Edit `backend/main.py`, line 188:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

**Frontend (change port):**
```bash
cd frontend
PORT=3001 npm run dev
```

### CORS errors
Make sure:
1. Backend is running on port 8000
2. Frontend is running on port 3000
3. Both servers are running simultaneously

## 📊 API Testing

You can test the backend API directly:

### Health Check
```bash
curl http://localhost:8000/
```

### Analyze a Stock
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 🎓 Next Steps

Once you have the basic app running, you can:

1. **Customize the UI**: Edit files in `frontend/app/` and `frontend/components/`
2. **Add features**: Implement comparison mode, portfolio analysis
3. **Deploy**: Use Vercel (frontend) + Modal/Railway (backend)
4. **Add authentication**: Implement user accounts
5. **Save reports**: Add database for historical reports

## 📚 File Structure

```
trading-agent/
├── backend/
│   ├── main.py              # FastAPI app with routes
│   ├── websocket_handler.py # Real-time updates
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── page.tsx        # Main dashboard
│   │   ├── layout.tsx      # Root layout
│   │   └── globals.css     # Styles
│   ├── components/
│   │   ├── SearchBar.tsx   # Ticker input
│   │   └── AnalysisView.tsx # Results display
│   └── package.json        # Node dependencies
└── src/
    ├── agent.py            # LangGraph workflow
    ├── config.py           # Configuration
    └── mcp/                # Data sources
```

## 🆘 Need Help?

- Check `WEB_APP_README.md` for detailed documentation
- Review `README.md` for agent architecture
- Check `SETUP.md` for original CLI setup

## 🎉 Success!

If you see the beautiful landing page at `http://localhost:3000`, you're all set! 

Try analyzing your first stock and enjoy your AI-powered research assistant! 🚀

