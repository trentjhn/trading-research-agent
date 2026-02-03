# Trading Research Agent - Web Application

A beautiful, production-ready web application for AI-powered stock analysis.

## 🎨 Features

- **Beautiful Modern UI**: Built with Next.js 14, TypeScript, and Tailwind CSS
- **Real-time Analysis**: WebSocket support for live progress updates
- **Comprehensive Reports**: Tabbed interface for different analysis types
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Mode Support**: Automatic theme switching
- **Fast & Efficient**: Parallel analysis execution in under 10 seconds

## 🏗️ Architecture

```
trading-agent/
├── backend/              # FastAPI server
│   ├── main.py          # API routes (REST + WebSocket)
│   ├── websocket_handler.py
│   └── requirements.txt
├── frontend/            # Next.js 14 app
│   ├── app/            # App router pages
│   ├── components/     # React components
│   └── package.json
└── src/                # Existing agent code (reused)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Your Anthropic API key (already configured in `.env`)

### 1. Start the Backend

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Start FastAPI server
python main.py
```

The backend will run on `http://localhost:8000`

### 2. Start the Frontend

```bash
# Install frontend dependencies
cd frontend
npm install

# Start Next.js development server
npm run dev
```

The frontend will run on `http://localhost:3000`

### 3. Open Your Browser

Navigate to `http://localhost:3000` and start analyzing stocks!

## 📡 API Endpoints

### REST API

- `GET /` - Health check
- `POST /api/analyze` - Analyze a single stock
- `POST /api/compare` - Compare multiple stocks
- `POST /api/portfolio` - Analyze a portfolio

### WebSocket

- `WS /ws/analyze/{ticker}` - Real-time analysis streaming

## 🎯 Usage

1. **Enter a ticker symbol** (e.g., AAPL, TSLA, MSFT)
2. **Click "Analyze"** to start the AI-powered analysis
3. **View results** in the tabbed interface:
   - Final Report (synthesized recommendation)
   - Fundamental Analysis
   - Technical Analysis
   - Sentiment Analysis
   - Macroeconomic Context

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful component library
- **Recharts** - Data visualization
- **Framer Motion** - Smooth animations
- **React Markdown** - Render analysis reports

### Backend
- **FastAPI** - Modern Python web framework
- **WebSockets** - Real-time communication
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### AI & Data
- **Claude (Anthropic)** - AI analysis
- **LangGraph** - Workflow orchestration
- **yfinance** - Financial data
- **pandas/numpy** - Technical indicators

## 📊 Analysis Types

### 1. Fundamental Analysis
- Company financials and valuation
- Growth metrics (revenue, earnings)
- Profitability ratios
- Analyst price targets

### 2. Technical Analysis
- Price trends (SMA 20, 50, 200)
- Momentum indicators (RSI)
- Volatility (Bollinger Bands)
- MACD signals

### 3. Sentiment Analysis
- Recent news headlines
- Market perception
- Aggregate sentiment score

### 4. Macroeconomic Context
- Interest rate outlook
- Inflation trends
- GDP growth
- Market conditions

## 🔮 Future Enhancements

- [ ] User authentication and accounts
- [ ] Save and favorite reports
- [ ] Watchlist management
- [ ] Portfolio tracking
- [ ] Real-time alerts
- [ ] Comparison tools
- [ ] Historical report archive
- [ ] Export to PDF
- [ ] Mobile app

## 🐛 Troubleshooting

### Backend won't start
- Make sure you're in the `backend/` directory
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify your `.env` file has the Anthropic API key

### Frontend won't start
- Make sure you're in the `frontend/` directory
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 18+)

### CORS errors
- Make sure both backend (8000) and frontend (3000) are running
- Check that the backend CORS settings allow `http://localhost:3000`

## 📝 License

This project is for personal use and educational purposes.

## 🙏 Acknowledgments

- Built with Claude AI (Anthropic)
- Financial data from Yahoo Finance
- UI components from shadcn/ui

