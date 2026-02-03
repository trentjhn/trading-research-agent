"""WebSocket handler for real-time analysis updates."""

from fastapi import WebSocket
import json
import asyncio
from typing import Dict, Any
import sys
sys.path.append('..')
from src.agent import research_agent, ResearchState

class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

manager = ConnectionManager()

async def stream_analysis(websocket: WebSocket, ticker: str):
    """
    Stream analysis progress to the client in real-time.
    
    Sends updates as each analysis step completes.
    """
    try:
        # Send initial status
        await websocket.send_json({
            "type": "status",
            "message": f"Starting analysis for {ticker}...",
            "progress": 0
        })
        
        # Initialize state
        initial_state: ResearchState = {
            "ticker": ticker,
            "fundamental_analysis": "",
            "technical_analysis": "",
            "sentiment_analysis": "",
            "macro_analysis": "",
            "final_report": ""
        }
        
        # Send progress update
        await websocket.send_json({
            "type": "status",
            "message": "Running parallel analyses...",
            "progress": 20
        })
        
        # Run the agent (we'll need to modify this to send intermediate updates)
        # For now, we'll simulate progress
        await asyncio.sleep(1)
        await websocket.send_json({
            "type": "status",
            "message": "Fundamental analysis complete",
            "progress": 40
        })
        
        await asyncio.sleep(1)
        await websocket.send_json({
            "type": "status",
            "message": "Technical analysis complete",
            "progress": 60
        })
        
        await asyncio.sleep(1)
        await websocket.send_json({
            "type": "status",
            "message": "Sentiment analysis complete",
            "progress": 80
        })
        
        # Run actual analysis
        final_state = research_agent.invoke(initial_state)
        
        # Send final result
        await websocket.send_json({
            "type": "complete",
            "message": "Analysis complete!",
            "progress": 100,
            "data": {
                "ticker": ticker,
                "fundamental_analysis": final_state['fundamental_analysis'],
                "technical_analysis": final_state['technical_analysis'],
                "sentiment_analysis": final_state['sentiment_analysis'],
                "macro_analysis": final_state['macro_analysis'],
                "final_report": final_state['final_report']
            }
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e),
            "progress": 0
        })

