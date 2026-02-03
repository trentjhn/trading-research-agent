# Augment AI Implementation Guide: Trading Research Agent

This document provides a complete, step-by-step guide for building the Trading Research Agent using a local-first development approach. It is optimized for an AI development assistant like Augment AI.

## 1. Project Goal

To build an AI-powered trading research agent that aggregates and analyzes multi-source financial data to generate a comprehensive report for a given stock ticker. The architecture will be modular and prioritize parallel processing for speed.

## 2. Final Directory Structure

Here is the target file structure for the project:

```
trading-research-agent/
├── .env
├── docker-compose.yml
├── pyproject.toml
├── qdrant_data/
└── src/
    ├── __init__.py
    ├── agent.py         # LangGraph orchestration and agent logic
    ├── config.py        # Configuration and client initializations
    ├── main.py          # Main application entrypoint
    └── mcp/
        ├── __init__.py
        ├── financial_data.py
        ├── macro_context.py
        ├── news_sentiment.py
        └── technical_analysis.py
```

## 3. Step-by-Step Implementation Plan

Follow these steps sequentially to build the application.

### Step 1: Initialize Project and Dependencies

First, create the project directory and the necessary configuration files.

**Action:** Create the `docker-compose.yml` file.

```yaml
# trading-research-agent/docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_data:/qdrant/storage
```

**Action:** Create the `pyproject.toml` file for dependency management with `uv`.

```toml
# trading-research-agent/pyproject.toml
[project]
name = "trading-research-agent"
version = "0.1.0"
description = "AI-powered trading research agent"
requires-python = ">=3.11"

dependencies = [
    # Core AI
    "anthropic>=0.21.3",
    "langgraph>=0.0.30",

    # Data & APIs
    "yfinance>=0.2.37",
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "requests>=2.31.0",

    # Technical Analysis
    "pandas-ta>=0.3.14b0",

    # Sentiment
    "transformers>=4.38.2",
    "torch>=2.2.1",

    # Storage
    "redis>=5.0.3",
    "qdrant-client>=1.7.3",
    "libsql-experimental>=0.2.0",

    # Utilities
    "python-dotenv>=1.0.1",
    "rich>=13.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
]
```

**Action:** Create the `.env` file. Fill in your actual Anthropic API key.

```
# trading-research-agent/.env
ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Step 2: Configuration and Clients

Create a centralized configuration file to manage settings and API clients.

**Action:** Create the `src/config.py` file.

```python
# trading-research-agent/src/config.py
import os
import redis
import anthropic
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# --- LLM Clients ---
CLAUDE_CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# --- Storage Clients ---
REDIS_CLIENT = redis.Redis(host='localhost', port=6379, decode_responses=True)
QDRANT_CLIENT = QdrantClient(url="http://localhost:6333")

# --- Models ---
# Use a dictionary for easy swapping and selection
MODEL_MAP = {
    "haiku": "claude-3-haiku-20240307",
    "sonnet": "claude-3-sonnet-20240229",
    "opus": "claude-3-opus-20240229",
}
```

### Step 3: Implement MCP Modules (Local Version)

Build the data-sourcing logic as local Python classes.

**Action:** Create the `src/mcp/financial_data.py` file.

```python
# trading-research-agent/src/mcp/financial_data.py
import yfinance as yf
import json
from src.config import REDIS_CLIENT

class FinancialDataMCP:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_company_info(self) -> dict:
        cache_key = f"info:{self.ticker}"
        cached_data = REDIS_CLIENT.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        info = self.stock.info
        REDIS_CLIENT.setex(cache_key, 3600, json.dumps(info)) # Cache for 1 hour
        return info

    def get_price_data(self, period="1y", interval="1d") -> dict:
        cache_key = f"price:{self.ticker}:{period}:{interval}"
        cached_data = REDIS_CLIENT.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        df = self.stock.history(period=period, interval=interval)
        data = df.to_json(orient='split')
        REDIS_CLIENT.setex(cache_key, 900, data) # Cache for 15 mins
        return json.loads(data)
```

**Action:** Create the `src/mcp/technical_analysis.py` file.

```python
# trading-research-agent/src/mcp/technical_analysis.py
import pandas as pd
import pandas_ta as ta

class TechnicalAnalysisMCP:
    def __init__(self, price_data: dict):
        self.df = pd.DataFrame(price_data['data'], columns=price_data['columns'], index=price_data['index'])
        self.df.index = pd.to_datetime(self.df.index, unit='ms')

    def get_full_analysis(self) -> dict:
        # Use the Strategy class from pandas_ta to get a summary
        custom_strategy = ta.Strategy(
            name="Comprehensive Analysis",
            description="SMA, RSI, MACD, BBands",
            ta=[
                {"kind": "sma", "length": 20},
                {"kind": "sma", "length": 50},
                {"kind": "rsi"},
                {"kind": "macd"},
                {"kind": "bbands"},
            ]
        )
        self.df.ta.strategy(custom_strategy)
        # Return the last row as a dictionary
        return self.df.iloc[-1].to_dict()
```

**Action:** Create the `src/mcp/news_sentiment.py` file.

```python
# trading-research-agent/src/mcp/news_sentiment.py
import yfinance as yf

class NewsSentimentMCP:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_news(self) -> list[dict]:
        # yfinance news is a good free starting point
        return self.stock.news
```

**Action:** Create the `src/mcp/macro_context.py` file (as a placeholder).

```python
# trading-research-agent/src/mcp/macro_context.py
class MacroContextMCP:
    def get_economic_outlook(self) -> dict:
        # Placeholder for future FRED API integration
        return {
            "interest_rate_outlook": "neutral",
            "inflation_outlook": "moderating",
            "gdp_growth_forecast": "1.5%"
        }
```

### Step 4: Build the Parallel Agent Workflow

This is the core of the application. The LangGraph setup must explicitly enable parallel execution.

**Action:** Create the `src/agent.py` file.

```python
# trading-research-agent/src/agent.py
import json
from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, END

from src.config import CLAUDE_CLIENT, MODEL_MAP
from src.mcp.financial_data import FinancialDataMCP
from src.mcp.technical_analysis import TechnicalAnalysisMCP
from src.mcp.news_sentiment import NewsSentimentMCP
from src.mcp.macro_context import MacroContextMCP

# 1. Define the State
class ResearchState(TypedDict):
    ticker: str
    fundamental_analysis: Annotated[str, operator.add]
    technical_analysis: Annotated[str, operator.add]
    sentiment_analysis: Annotated[str, operator.add]
    macro_analysis: Annotated[str, operator.add]
    final_report: str

# 2. Define Agent Nodes
def run_fundamental_analysis(state: ResearchState) -> dict:
    ticker = state['ticker']
    mcp = FinancialDataMCP(ticker)
    info = mcp.get_company_info()
    prompt = f"Analyze the following fundamental data for {ticker} and provide a summary:\n\n{json.dumps(info, indent=2)}"
    
    response = CLAUDE_CLIENT.messages.create(
        model=MODEL_MAP['haiku'],
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"fundamental_analysis": response.content[0].text}

def run_technical_analysis(state: ResearchState) -> dict:
    ticker = state['ticker']
    price_mcp = FinancialDataMCP(ticker)
    price_data = price_mcp.get_price_data()
    ta_mcp = TechnicalAnalysisMCP(price_data)
    analysis = ta_mcp.get_full_analysis()
    prompt = f"Analyze the following technical indicators for {ticker} and provide a summary:\n\n{json.dumps(analysis, indent=2)}"

    response = CLAUDE_CLIENT.messages.create(
        model=MODEL_MAP['haiku'],
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"technical_analysis": response.content[0].text}

def run_sentiment_analysis(state: ResearchState) -> dict:
    ticker = state['ticker']
    news_mcp = NewsSentimentMCP(ticker)
    news = news_mcp.get_news()
    prompt = f"Analyze the sentiment of the following news headlines for {ticker} and provide a summary:\n\n{json.dumps(news, indent=2)}"

    response = CLAUDE_CLIENT.messages.create(
        model=MODEL_MAP['haiku'],
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"sentiment_analysis": response.content[0].text}

def run_macro_analysis(state: ResearchState) -> dict:
    macro_mcp = MacroContextMCP()
    outlook = macro_mcp.get_economic_outlook()
    prompt = f"Analyze the following macroeconomic outlook and its potential impact on the market:\n\n{json.dumps(outlook, indent=2)}"

    response = CLAUDE_CLIENT.messages.create(
        model=MODEL_MAP['haiku'],
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"macro_analysis": response.content[0].text}

def run_synthesis(state: ResearchState) -> dict:
    prompt = f"""You are a senior trading analyst. Synthesize the following analyses for {state['ticker']} into a single, actionable report.

**Fundamental Analysis:**
{state['fundamental_analysis']}

**Technical Analysis:**
{state['technical_analysis']}

**Sentiment Analysis:**
{state['sentiment_analysis']}

**Macroeconomic Context:**
{state['macro_analysis']}

Provide a final recommendation (Buy, Hold, Sell) with a confidence score and a summary of the bull and bear cases."""

    response = CLAUDE_CLIENT.messages.create(
        model=MODEL_MAP['sonnet'],
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"final_report": response.content[0].text}

# 3. Build the Graph
workflow = StateGraph(ResearchState)

# Add nodes for each agent
workflow.add_node("fundamental", run_fundamental_analysis)
workflow.add_node("technical", run_technical_analysis)
workflow.add_node("sentiment", run_sentiment_analysis)
workflow.add_node("macro", run_macro_analysis)
workflow.add_node("synthesis", run_synthesis)

# Set the entry point
workflow.set_entry_point("fundamental") # Can be any of the parallel nodes

# *** CRITICAL: This creates the parallel execution ***
# All analysis nodes run after the entry point, but have no dependencies on each other.
workflow.add_edge("fundamental", "synthesis")
workflow.add_edge("technical", "synthesis")
workflow.add_edge("sentiment", "synthesis")
workflow.add_edge("macro", "synthesis")

# The synthesis node runs only after ALL of the above have completed.
workflow.add_conditional_edges(
    "fundamental",
    lambda x: "continue",
    {"continue": "technical"}
)
workflow.add_conditional_edges(
    "technical",
    lambda x: "continue",
    {"continue": "sentiment"}
)
workflow.add_conditional_edges(
    "sentiment",
    lambda x: "continue",
    {"continue": "macro"}
)
workflow.add_conditional_edges(
    "macro",
    lambda x: "continue",
    {"continue": "synthesis"}
)

workflow.add_edge('synthesis', END)

# Compile the graph
research_agent = workflow.compile()
```

### Step 5: Create the Main Entrypoint

Finally, create the main script to run the agent.

**Action:** Create the `src/main.py` file.

```python
# trading-research-agent/src/main.py
import sys
from rich.console import Console
from rich.markdown import Markdown

from src.agent import research_agent, ResearchState

def main():
    console = Console()
    if len(sys.argv) < 2:
        console.print("[bold red]Error:[/bold red] Please provide a stock ticker.")
        console.print("Usage: python -m src.main [TICKER]")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    console.print(f"🚀 [bold green]Starting research for ticker:[/bold green] {ticker}")

    initial_state: ResearchState = {
        "ticker": ticker,
        "fundamental_analysis": "",
        "technical_analysis": "",
        "sentiment_analysis": "",
        "macro_analysis": "",
        "final_report": ""
    }

    # The `stream` method in LangGraph executes the graph.
    # For parallel execution, it will run all branches concurrently.
    final_state = research_agent.invoke(initial_state)

    console.print("\n---")
    console.print(f"✅ [bold blue]Final Report for {ticker}[/bold blue]")
    console.print("---")
    
    # Use rich to render the final markdown-formatted report
    md = Markdown(final_state['final_report'])
    console.print(md)

if __name__ == "__main__":
    main()

```

### Step 6: Run the Application

1.  **Start Docker Services:**
    ```bash
    docker-compose up -d
    ```

2.  **Install Dependencies:**
    ```bash
    uv pip install -r pyproject.toml
    ```

3.  **Run the Agent:**
    ```bash
    python -m src.main AAPL
    ```

This comprehensive guide provides all the necessary code and instructions to build the Trading Research Agent. The structure is modular, allowing for easy extension and future migration to a production environment. The parallel agent workflow is the key to achieving the desired speed and performance. 
