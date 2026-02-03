# Trading Research Agent

An AI-powered trading research agent that generates comprehensive investment reports by running parallel analyses on stocks.

## 🌐 Web Application

**NEW!** Beautiful web interface with real-time analysis streaming!

```bash
./start-webapp.sh
```

Then open **http://localhost:3000** in your browser.

See [WEB_APP_README.md](WEB_APP_README.md) for full web app documentation.

## Features

- **Parallel Execution**: Runs 4 independent analyses simultaneously for maximum speed
  - Fundamental Analysis (financials, valuation, growth metrics)
  - Technical Analysis (price trends, RSI, MACD, Bollinger Bands)
  - Sentiment Analysis (news headlines, market perception)
  - Macroeconomic Analysis (market conditions, economic outlook)
- **AI-Powered Synthesis**: Uses Claude Sonnet to synthesize all analyses into actionable investment reports
- **Redis Caching**: Caches API responses to avoid redundant calls and respect rate limits
- **Rich CLI Interface**: Beautiful terminal output with progress indicators and formatted reports
- **Web Interface**: Next.js 14 frontend with FastAPI backend

## Architecture

The agent uses **LangGraph** for workflow orchestration with a true parallel execution pattern:

```
START
  ├─> Fundamental Analysis ─┐
  ├─> Technical Analysis ────┤
  ├─> Sentiment Analysis ────┼─> Synthesis ─> END
  └─> Macro Analysis ────────┘
```

All 4 analysis nodes run in parallel, and the synthesis node waits for all of them to complete before generating the final report.

## Prerequisites

- Python 3.9+
- Node.js 16+ (for web app)
- Docker and Docker Compose (optional, for caching)
- Anthropic API key

## Quick Start

### Web App (Recommended)

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 2. Install dependencies
cd backend && pip3 install -r requirements.txt --user && cd ..
cd frontend && npm install && cd ..

# 3. Start the app
./start-webapp.sh

# 4. Open http://localhost:3000
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

### CLI Only

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 2. Install dependencies
pip install -e .

# 3. Run analysis
python3 -m src.main AAPL
```

## Usage

### Web Interface

1. Open http://localhost:3000
2. Enter a stock ticker (e.g., AAPL, TSLA, MSFT)
3. Click "Analyze"
4. View comprehensive AI-powered report

### CLI

Run the agent with any stock ticker:

```bash
python3 -m src.main AAPL
```

Example output:
```
🚀 Trading Research Agent
Starting comprehensive research analysis for: AAPL

Running 4 parallel analyses:
  • Fundamental Analysis (financials, valuation)
  • Technical Analysis (price trends, indicators)
  • Sentiment Analysis (news, market perception)
  • Macroeconomic Analysis (market conditions)

  🔍 Running fundamental analysis for AAPL...
  📊 Running technical analysis for AAPL...
  📰 Running sentiment analysis for AAPL...
  🌍 Running macro analysis...
  ✅ Fundamental analysis complete
  ✅ Technical analysis complete
  ✅ Sentiment analysis complete
  ✅ Macro analysis complete
  🎯 Synthesizing final report for AAPL...
  ✅ Synthesis complete

✓ Analysis complete in 12.34 seconds

# Investment Report: AAPL

## Executive Summary
[AI-generated summary]

## Recommendation
**Action:** BUY / HOLD / SELL
**Confidence:** High / Medium / Low

## Bull Case
[Key positive points]

## Bear Case
[Key negative points]

## Key Takeaways
[Important insights]

## Risk Factors
[Main risks to monitor]
```

## Project Structure

```
trading-research-agent/
├── backend/                # FastAPI backend
│   ├── main.py            # REST API + WebSocket
│   ├── websocket_handler.py
│   └── requirements.txt
├── frontend/              # Next.js 14 frontend
│   ├── app/              # Pages and layouts
│   ├── components/       # React components
│   └── package.json
├── src/                   # Core agent
│   ├── agent.py          # LangGraph workflow
│   ├── config.py         # Configuration
│   ├── main.py           # CLI entrypoint
│   └── mcp/              # Data source modules
├── start-webapp.sh       # Start web app
├── WEB_APP_README.md     # Web app docs
└── README.md             # This file
```

## How It Works

1. **User Input**: Provide a stock ticker (e.g., `AAPL`)
2. **Parallel Data Collection**: 4 MCP modules fetch data simultaneously:
   - Financial data from yfinance
   - Price history for technical analysis
   - Recent news headlines
   - Macroeconomic context
3. **AI Analysis**: Each module's data is analyzed by Claude Haiku (fast, cost-effective)
4. **Synthesis**: Claude Sonnet combines all analyses into a comprehensive report
5. **Output**: Formatted markdown report with actionable recommendations

## Documentation

- [WEB_APP_README.md](WEB_APP_README.md) - Complete web app guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [INSTALL_WEBAPP.md](INSTALL_WEBAPP.md) - Installation instructions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [SETUP.md](SETUP.md) - Detailed setup guide

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

### Quick Fixes

**Website can't be reached:**
```bash
cd frontend && npm install && cd ..
./start-webapp.sh
```

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

## License

MIT

## Disclaimer

This tool is for informational and educational purposes only. It is not financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.
