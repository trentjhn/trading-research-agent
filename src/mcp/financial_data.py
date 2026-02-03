"""Financial data MCP module - fetches company info and price data."""

import yfinance as yf
import json
from typing import Optional
from src.config import REDIS_CLIENT, CACHE_TTL_COMPANY_INFO, CACHE_TTL_PRICE_DATA


class FinancialDataMCP:
    """Fetches and caches financial data using yfinance."""
    
    def __init__(self, ticker: str):
        """
        Initialize the financial data MCP.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        """
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)

    def get_company_info(self) -> dict:
        """
        Fetch company information with Redis caching.
        
        Returns:
            Dictionary containing company info (sector, industry, market cap, etc.)
        """
        cache_key = f"info:{self.ticker}"
        
        # Try to get from cache
        if REDIS_CLIENT:
            try:
                cached_data = REDIS_CLIENT.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Cache read error: {e}")

        # Fetch fresh data
        try:
            info = self.stock.info
            
            # Cache the result
            if REDIS_CLIENT:
                try:
                    REDIS_CLIENT.setex(
                        cache_key, 
                        CACHE_TTL_COMPANY_INFO, 
                        json.dumps(info)
                    )
                except Exception as e:
                    print(f"Cache write error: {e}")
            
            return info
        except Exception as e:
            raise ValueError(f"Failed to fetch company info for {self.ticker}: {e}")

    def get_price_data(self, period: str = "1y", interval: str = "1d") -> dict:
        """
        Fetch historical price data with Redis caching.
        
        Args:
            period: Time period (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval: Data interval (e.g., '1m', '5m', '1h', '1d', '1wk', '1mo')
            
        Returns:
            Dictionary with price data in split-oriented format
        """
        cache_key = f"price:{self.ticker}:{period}:{interval}"
        
        # Try to get from cache
        if REDIS_CLIENT:
            try:
                cached_data = REDIS_CLIENT.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Cache read error: {e}")

        # Fetch fresh data
        try:
            df = self.stock.history(period=period, interval=interval)
            
            if df.empty:
                raise ValueError(f"No price data available for {self.ticker}")
            
            # Convert to JSON-serializable format
            data = df.to_json(orient='split')
            
            # Cache the result
            if REDIS_CLIENT:
                try:
                    REDIS_CLIENT.setex(
                        cache_key, 
                        CACHE_TTL_PRICE_DATA, 
                        data
                    )
                except Exception as e:
                    print(f"Cache write error: {e}")
            
            return json.loads(data)
        except Exception as e:
            raise ValueError(f"Failed to fetch price data for {self.ticker}: {e}")

