"""LangGraph agent orchestration with parallel execution."""

import json
from typing import TypedDict
from langgraph.graph import StateGraph

from src.config import CLAUDE_CLIENT, MODEL_MAP
from src.mcp.financial_data import FinancialDataMCP
from src.mcp.technical_analysis import TechnicalAnalysisMCP
from src.mcp.news_sentiment import NewsSentimentMCP
from src.mcp.macro_context import MacroContextMCP


# ============================================================================
# STATE DEFINITION
# ============================================================================

class ResearchState(TypedDict):
    """State for the research agent workflow."""
    ticker: str
    fundamental_analysis: str
    technical_analysis: str
    sentiment_analysis: str
    macro_analysis: str
    final_report: str


# ============================================================================
# AGENT NODES - Each runs independently in parallel
# ============================================================================

def run_fundamental_analysis(state: ResearchState) -> dict:
    """Analyze fundamental data (financials, valuation, company info)."""
    ticker = state['ticker']
    print(f"  🔍 Running fundamental analysis for {ticker}...")
    
    try:
        mcp = FinancialDataMCP(ticker)
        info = mcp.get_company_info()
        
        # Extract key metrics for analysis
        key_metrics = {
            "company_name": info.get("longName", ticker),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "price_to_book": info.get("priceToBook", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "profit_margins": info.get("profitMargins", "N/A"),
            "revenue_growth": info.get("revenueGrowth", "N/A"),
            "earnings_growth": info.get("earningsGrowth", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "target_mean_price": info.get("targetMeanPrice", "N/A"),
            "recommendation": info.get("recommendationKey", "N/A"),
        }
        
        prompt = f"""Analyze the following fundamental data for {ticker} and provide a concise summary.

Company: {key_metrics['company_name']}
Sector: {key_metrics['sector']} | Industry: {key_metrics['industry']}

Key Metrics:
- Market Cap: {key_metrics['market_cap']}
- P/E Ratio: {key_metrics['pe_ratio']} | Forward P/E: {key_metrics['forward_pe']}
- Price/Book: {key_metrics['price_to_book']}
- Dividend Yield: {key_metrics['dividend_yield']}
- Profit Margins: {key_metrics['profit_margins']}
- Revenue Growth: {key_metrics['revenue_growth']}
- Earnings Growth: {key_metrics['earnings_growth']}
- Current Price: {key_metrics['current_price']}
- Analyst Target: {key_metrics['target_mean_price']}
- Analyst Recommendation: {key_metrics['recommendation']}

Provide a 3-4 sentence analysis covering:
1. Valuation assessment (cheap/fair/expensive)
2. Growth profile
3. Key strengths or concerns"""

        response = CLAUDE_CLIENT.messages.create(
            model=MODEL_MAP['haiku'],
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        analysis = response.content[0].text
        print(f"  ✅ Fundamental analysis complete")
        return {"fundamental_analysis": analysis}
        
    except Exception as e:
        error_msg = f"Error in fundamental analysis: {str(e)}"
        print(f"  ❌ {error_msg}")
        return {"fundamental_analysis": error_msg}


def run_technical_analysis(state: ResearchState) -> dict:
    """Analyze technical indicators and price trends."""
    ticker = state['ticker']
    print(f"  📊 Running technical analysis for {ticker}...")

    try:
        price_mcp = FinancialDataMCP(ticker)
        price_data = price_mcp.get_price_data()
        ta_mcp = TechnicalAnalysisMCP(price_data)
        analysis = ta_mcp.get_full_analysis()

        # Format for readability
        formatted_analysis = {
            "current_price": analysis.get("Close"),
            "sma_20": analysis.get("SMA_20"),
            "sma_50": analysis.get("SMA_50"),
            "sma_200": analysis.get("SMA_200"),
            "rsi": analysis.get("RSI_14"),
            "macd": analysis.get("MACD_12_26_9"),
            "macd_signal": analysis.get("MACDs_12_26_9"),
            "bb_upper": analysis.get("BBU_5_2.0"),
            "bb_middle": analysis.get("BBM_5_2.0"),
            "bb_lower": analysis.get("BBL_5_2.0"),
            "trend_signal": analysis.get("trend_signal"),
            "momentum_signal": analysis.get("momentum_signal"),
        }

        prompt = f"""Analyze the following technical indicators for {ticker} and provide a concise summary.

Technical Indicators:
- Current Price: {formatted_analysis['current_price']}
- SMA 20: {formatted_analysis['sma_20']}
- SMA 50: {formatted_analysis['sma_50']}
- SMA 200: {formatted_analysis['sma_200']}
- RSI (14): {formatted_analysis['rsi']}
- MACD: {formatted_analysis['macd']}
- MACD Signal: {formatted_analysis['macd_signal']}
- Bollinger Bands: Upper={formatted_analysis['bb_upper']}, Middle={formatted_analysis['bb_middle']}, Lower={formatted_analysis['bb_lower']}
- Trend Signal: {formatted_analysis['trend_signal']}
- Momentum Signal: {formatted_analysis['momentum_signal']}

Provide a 3-4 sentence analysis covering:
1. Current trend (bullish/bearish/neutral)
2. Momentum and overbought/oversold conditions
3. Key support/resistance levels"""

        response = CLAUDE_CLIENT.messages.create(
            model=MODEL_MAP['haiku'],
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis_text = response.content[0].text
        print(f"  ✅ Technical analysis complete")
        return {"technical_analysis": analysis_text}

    except Exception as e:
        error_msg = f"Error in technical analysis: {str(e)}"
        print(f"  ❌ {error_msg}")
        return {"technical_analysis": error_msg}


def run_sentiment_analysis(state: ResearchState) -> dict:
    """Analyze news sentiment and market perception."""
    ticker = state['ticker']
    print(f"  📰 Running sentiment analysis for {ticker}...")

    try:
        news_mcp = NewsSentimentMCP(ticker)
        news = news_mcp.get_news()

        # Format news for analysis
        news_summary = []
        for i, article in enumerate(news[:10], 1):
            news_summary.append(f"{i}. {article['title']} ({article['publisher']})")

        news_text = "\n".join(news_summary)

        prompt = f"""Analyze the sentiment of the following recent news headlines for {ticker}.

Recent News:
{news_text}

Provide a 3-4 sentence analysis covering:
1. Overall sentiment (positive/neutral/negative)
2. Key themes or narratives
3. Potential impact on stock price"""

        response = CLAUDE_CLIENT.messages.create(
            model=MODEL_MAP['haiku'],
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = response.content[0].text
        print(f"  ✅ Sentiment analysis complete")
        return {"sentiment_analysis": analysis}

    except Exception as e:
        error_msg = f"Error in sentiment analysis: {str(e)}"
        print(f"  ❌ {error_msg}")
        return {"sentiment_analysis": error_msg}


def run_macro_analysis(state: ResearchState) -> dict:
    """Analyze macroeconomic context and market conditions."""
    print(f"  🌍 Running macro analysis...")

    try:
        macro_mcp = MacroContextMCP()
        outlook = macro_mcp.get_economic_outlook()

        prompt = f"""Analyze the following macroeconomic outlook and its potential impact on the stock market.

Economic Outlook:
- Interest Rates: {outlook['interest_rate_outlook']} - {outlook['interest_rate_note']}
- Inflation: {outlook['inflation_outlook']} - {outlook['inflation_note']}
- GDP Growth: {outlook['gdp_growth_forecast']} - {outlook['gdp_note']}
- Employment: {outlook['employment_outlook']} - {outlook['employment_note']}
- Market Regime: {outlook['market_regime']}
- Key Risks: {', '.join(outlook['key_risks'])}

Provide a 3-4 sentence analysis covering:
1. Overall market environment (favorable/neutral/challenging)
2. Key macro factors to watch
3. Implications for equity investors"""

        response = CLAUDE_CLIENT.messages.create(
            model=MODEL_MAP['haiku'],
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = response.content[0].text
        print(f"  ✅ Macro analysis complete")
        return {"macro_analysis": analysis}

    except Exception as e:
        error_msg = f"Error in macro analysis: {str(e)}"
        print(f"  ❌ {error_msg}")
        return {"macro_analysis": error_msg}


def run_synthesis(state: ResearchState) -> dict:
    """Synthesize all analyses into a final actionable report."""
    ticker = state['ticker']
    print(f"  🎯 Synthesizing final report for {ticker}...")

    prompt = f"""You are a senior trading analyst. Synthesize the following analyses for {ticker} into a single, actionable investment report.

**Fundamental Analysis:**
{state['fundamental_analysis']}

**Technical Analysis:**
{state['technical_analysis']}

**Sentiment Analysis:**
{state['sentiment_analysis']}

**Macroeconomic Context:**
{state['macro_analysis']}

Provide a comprehensive report with the following structure:

# Investment Report: {ticker}

## Executive Summary
[2-3 sentence overview of the investment thesis]

## Recommendation
**Action:** [BUY / HOLD / SELL]
**Confidence:** [High / Medium / Low]
**Price Target:** [If applicable]

## Bull Case
[3-4 key points supporting a positive outlook]

## Bear Case
[3-4 key points supporting a negative outlook]

## Key Takeaways
[3-5 bullet points with the most important insights]

## Risk Factors
[2-3 main risks to monitor]

Keep the report concise, actionable, and data-driven."""

    try:
        response = CLAUDE_CLIENT.messages.create(
            model=MODEL_MAP['haiku'],  # Using Haiku for synthesis (faster and more reliable)
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

        report = response.content[0].text
        print("  ✅ Synthesis complete")
        return {"final_report": report}

    except Exception as e:
        error_msg = f"Error in synthesis: {str(e)}"
        print(f"  ❌ {error_msg}")
        return {"final_report": error_msg}


# ============================================================================
# GRAPH CONSTRUCTION - CRITICAL: TRUE PARALLEL EXECUTION
# ============================================================================

def build_research_agent():
    """
    Build the LangGraph workflow with TRUE parallel execution.

    KEY INSIGHT: In LangGraph, when multiple nodes all have edges pointing to
    the same target node, they execute in PARALLEL. The target node waits for
    ALL of them to complete before executing.

    For our use case:
    - START fans out to 4 analysis nodes (fundamental, technical, sentiment, macro)
    - All 4 run in parallel
    - All 4 point to synthesis
    - Synthesis waits for all 4 to complete, then runs
    - Synthesis points to END
    """
    workflow = StateGraph(ResearchState)

    # Add all analysis nodes
    workflow.add_node("fundamental", run_fundamental_analysis)
    workflow.add_node("technical", run_technical_analysis)
    workflow.add_node("sentiment", run_sentiment_analysis)
    workflow.add_node("macro", run_macro_analysis)
    workflow.add_node("synthesis", run_synthesis)

    # PARALLEL EXECUTION PATTERN:
    # Connect START to all 4 analysis nodes - they will run in parallel
    workflow.add_edge("__start__", "fundamental")
    workflow.add_edge("__start__", "technical")
    workflow.add_edge("__start__", "sentiment")
    workflow.add_edge("__start__", "macro")

    # All 4 analysis nodes connect to synthesis
    # Synthesis will wait for ALL 4 to complete before running
    workflow.add_edge("fundamental", "synthesis")
    workflow.add_edge("technical", "synthesis")
    workflow.add_edge("sentiment", "synthesis")
    workflow.add_edge("macro", "synthesis")

    # Synthesis is the final step
    workflow.add_edge("synthesis", "__end__")

    # Compile the graph
    return workflow.compile()


# Create the compiled agent
research_agent = build_research_agent()

