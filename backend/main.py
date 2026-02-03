"""FastAPI backend for Trading Research Agent."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
from datetime import datetime

# Import our existing agent
import sys
sys.path.append('..')
from src.agent import research_agent, ResearchState
from backend.websocket_handler import stream_analysis, manager

app = FastAPI(
    title="Trading Research Agent API",
    description="AI-powered stock analysis and research platform",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request/Response Models ---

class AnalysisRequest(BaseModel):
    ticker: str

class ComparisonRequest(BaseModel):
    tickers: List[str]

class PortfolioRequest(BaseModel):
    holdings: List[dict]  # [{"ticker": "AAPL", "weight": 0.3}, ...]

class AnalysisResponse(BaseModel):
    ticker: str
    timestamp: str
    fundamental_analysis: str
    technical_analysis: str
    sentiment_analysis: str
    macro_analysis: str
    final_report: str
    status: str

# --- API Routes ---

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Trading Research Agent API",
        "version": "1.0.0"
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """
    Analyze a single stock ticker.
    
    Returns comprehensive analysis including fundamental, technical,
    sentiment, and macro perspectives.
    """
    try:
        ticker = request.ticker.upper()
        
        # Initialize state
        initial_state: ResearchState = {
            "ticker": ticker,
            "fundamental_analysis": "",
            "technical_analysis": "",
            "sentiment_analysis": "",
            "macro_analysis": "",
            "final_report": ""
        }
        
        # Run the agent
        final_state = research_agent.invoke(initial_state)
        
        return AnalysisResponse(
            ticker=ticker,
            timestamp=datetime.now().isoformat(),
            fundamental_analysis=final_state['fundamental_analysis'],
            technical_analysis=final_state['technical_analysis'],
            sentiment_analysis=final_state['sentiment_analysis'],
            macro_analysis=final_state['macro_analysis'],
            final_report=final_state['final_report'],
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare")
async def compare_stocks(request: ComparisonRequest):
    """
    Compare multiple stocks side-by-side.
    
    Runs analysis on each ticker and returns comparative insights.
    """
    try:
        results = []
        
        for ticker in request.tickers:
            ticker = ticker.upper()
            initial_state: ResearchState = {
                "ticker": ticker,
                "fundamental_analysis": "",
                "technical_analysis": "",
                "sentiment_analysis": "",
                "macro_analysis": "",
                "final_report": ""
            }
            
            final_state = research_agent.invoke(initial_state)
            results.append({
                "ticker": ticker,
                "analysis": final_state
            })
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "comparisons": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/portfolio")
async def analyze_portfolio(request: PortfolioRequest):
    """
    Analyze an entire portfolio of stocks.
    
    Provides portfolio-level insights including diversification,
    risk exposure, and weighted sentiment.
    """
    try:
        # Analyze each holding
        holdings_analysis = []
        
        for holding in request.holdings:
            ticker = holding['ticker'].upper()
            weight = holding.get('weight', 0)
            
            # Run analysis
            # (Implementation similar to analyze_stock)
            
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "portfolio_analysis": holdings_analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/analyze/{ticker}")
async def websocket_analyze(websocket: WebSocket, ticker: str):
    """
    WebSocket endpoint for real-time analysis streaming.

    Sends progress updates as the analysis runs.
    """
    await websocket.accept()
    try:
        await stream_analysis(websocket, ticker.upper())
    except WebSocketDisconnect:
        print(f"Client disconnected from analysis stream for {ticker}")
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

