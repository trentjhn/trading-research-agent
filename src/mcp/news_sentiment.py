"""News sentiment MCP module - fetches and analyzes news headlines."""

import yfinance as yf
from typing import List, Dict, Any


class NewsSentimentMCP:
    """Fetches news headlines using yfinance."""
    
    def __init__(self, ticker: str):
        """
        Initialize the news sentiment MCP.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        """
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)

    def get_news(self) -> List[Dict[str, Any]]:
        """
        Fetch recent news headlines for the ticker.
        
        Returns:
            List of news articles with title, publisher, link, and timestamp
        """
        try:
            news = self.stock.news
            
            if not news:
                return [{
                    "title": f"No recent news available for {self.ticker}",
                    "publisher": "N/A",
                    "link": "",
                    "providerPublishTime": None
                }]
            
            # Clean and format news data
            formatted_news = []
            for article in news[:10]:  # Limit to 10 most recent articles
                formatted_news.append({
                    "title": article.get("title", "No title"),
                    "publisher": article.get("publisher", "Unknown"),
                    "link": article.get("link", ""),
                    "providerPublishTime": article.get("providerPublishTime"),
                    "type": article.get("type", "article")
                })
            
            return formatted_news
            
        except Exception as e:
            print(f"Warning: Failed to fetch news for {self.ticker}: {e}")
            return [{
                "title": f"Error fetching news for {self.ticker}",
                "publisher": "Error",
                "link": "",
                "providerPublishTime": None,
                "error": str(e)
            }]

