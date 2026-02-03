# Trading Research Agent: Use Cases & Future Roadmap

This document outlines the core functionality of the Trading Research Agent as designed, and explores a roadmap of potential future use cases to expand its capabilities.

## 1. Core Use Case: Comprehensive Single-Asset Analysis

The primary and foundational use case of the agent is to perform a deep-dive analysis on a single publicly traded asset (like a stock or ETF) when given its ticker symbol. The agent is designed to be a "fire-and-forget" tool that autonomously gathers, analyzes, and synthesizes a multi-faceted report.

This core function is composed of four parallel sub-tasks, each representing a distinct analytical perspective:

| Agent / Use Case | Purpose | Data Sources (Local Dev) | Key Outputs |
| :--- | :--- | :--- | :--- |
| **Fundamental Analysis** | To assess the financial health, valuation, and intrinsic value of the company. | `yfinance` (Company Info) | Valuation summary, financial strengths/weaknesses, growth assessment. |
| **Technical Analysis** | To identify trends, patterns, and key price levels based on historical market data. | `yfinance` (Price History), `pandas-ta` | Trend identification (SMA, MACD), momentum (RSI), volatility (Bollinger Bands). |
| **News & Sentiment Analysis** | To gauge market perception and identify narratives by analyzing recent news coverage. | `yfinance` (News Headlines) | Aggregate sentiment score (positive/neutral/negative), summary of key news themes. |
| **Macroeconomic Analysis** | To understand the broader economic environment and its potential impact on the asset. | Placeholder (Future FRED API) | Outlook on interest rates, inflation, and GDP growth. |

Finally, the **Synthesis Agent** consolidates these four parallel analyses into a single, coherent, and actionable report, providing a final recommendation and a summary of the bull and bear cases.

## 2. Roadmap: Potential Extension Use Cases

The agent's modular MCP-based architecture is perfectly suited for future expansion. The following use cases represent logical next steps to evolve the tool from a single-asset analyzer into a more powerful and versatile investment research platform.

### Use Case 2.1: Comparative Analysis

-   **Description:** Instead of analyzing one ticker in isolation, the agent could compare two or more assets head-to-head. This is invaluable for deciding between two potential investments.
-   **Implementation:** The user would provide multiple tickers (e.g., `AAPL vs. MSFT`). The agent would run the full analysis pipeline for each ticker in parallel and then add a new **Comparative Synthesis** step. This final step would use a Claude Sonnet or Opus prompt to directly compare the fundamental, technical, and sentiment reports, highlighting relative strengths and weaknesses.

### Use Case 2.2: Portfolio-Level Analysis

-   **Description:** The agent could analyze an entire portfolio of assets provided by the user. This would provide a holistic view of the portfolio's overall health, risk exposure, and sentiment.
-   **Implementation:** The user would input a list of tickers and their respective weightings. The agent would run the analysis for each ticker. The Synthesis Agent would then be tasked with aggregating the results to calculate a weighted-average sentiment, identify correlated risks, and highlight the most and least promising assets within the portfolio.

### Use Case 2.3: Market Screener & Idea Generation

-   **Description:** Instead of starting with a ticker, the user could describe the *type* of company they are looking for. The agent would then screen the market to find matching candidates.
-   **Implementation:** This would require a new **Screener Agent** as the entry point. The user might prompt: "Find me tech stocks with a P/E ratio under 20 and a bullish RSI trend." The Screener Agent would use an API (like Financial Modeling Prep's screener) to get a list of candidate tickers. Then, it would pass this list to the existing parallel analysis workflow to perform a deeper dive on the top 5-10 results.

### Use Case 2.4: Real-Time Event Monitoring & Alerts

-   **Description:** The agent could be configured to run continuously in the background, monitoring a specific stock or a watchlist for significant events and sending an alert when one occurs.
-   **Implementation:** This would involve deploying the agent on a serverless platform like Modal and triggering it on a schedule (e.g., every 5 minutes). The agent would be modified to check for specific conditions, such as:
    -   A sudden spike in news volume.
    -   A significant change in sentiment score.
    -   A technical indicator crossing a key threshold (e.g., RSI entering overbought territory).
    -   If a condition is met, it would trigger a notification (e.g., via email or a messaging app).

### Use Case 2.5: Interactive Conversational Analysis

-   **Description:** After receiving the initial report, the user could ask follow-up questions in a conversational manner.
-   **Implementation:** This is the most complex extension and would involve moving from a single-run graph to a persistent, conversational agent. The state of the graph would need to be saved. When the user asks a follow-up like, "Tell me more about its revenue growth over the last 3 years," the agent would need to understand which MCP module to call (`FinancialDataMCP`) to get the necessary data and then generate a new response, all while maintaining the context of the original report.

This roadmap shows how the initial, well-architected agent can serve as a robust foundation for a suite of powerful investment research tools. Each extension builds upon the existing modular components, demonstrating the value of the initial design choices.
