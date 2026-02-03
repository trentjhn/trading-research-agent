"""Technical analysis MCP module - calculates technical indicators."""

import pandas as pd
import numpy as np
from typing import Dict, Any


class TechnicalAnalysisMCP:
    """Calculates technical indicators."""
    
    def __init__(self, price_data: dict):
        """
        Initialize the technical analysis MCP.
        
        Args:
            price_data: Price data in split-oriented format from FinancialDataMCP
        """
        # Convert from split-oriented JSON to DataFrame
        self.df = pd.DataFrame(
            price_data['data'], 
            columns=price_data['columns'], 
            index=price_data['index']
        )
        self.df.index = pd.to_datetime(self.df.index, unit='ms')
        
        # Ensure we have the required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

    def get_full_analysis(self) -> Dict[str, Any]:
        """
        Calculate comprehensive technical indicators.

        Returns:
            Dictionary containing the latest values of all technical indicators
        """
        try:
            # Calculate SMAs
            self.df['SMA_20'] = self.df['Close'].rolling(window=20).mean()
            self.df['SMA_50'] = self.df['Close'].rolling(window=50).mean()
            self.df['SMA_200'] = self.df['Close'].rolling(window=200).mean()

            # Calculate RSI
            self.df['RSI_14'] = self._calculate_rsi(self.df['Close'], 14)

            # Calculate MACD
            macd_data = self._calculate_macd(self.df['Close'])
            self.df['MACD'] = macd_data['macd']
            self.df['MACDh'] = macd_data['histogram']
            self.df['MACDs'] = macd_data['signal']

            # Calculate Bollinger Bands
            bb_data = self._calculate_bollinger_bands(self.df['Close'], 20, 2)
            self.df['BBL_20_2.0'] = bb_data['lower']
            self.df['BBM_20_2.0'] = bb_data['middle']
            self.df['BBU_20_2.0'] = bb_data['upper']

            # Get the most recent row (latest indicators)
            latest = self.df.iloc[-1]

            # Convert to dictionary, handling NaN values
            result = {}
            for key, value in latest.items():
                if pd.isna(value):
                    result[key] = None
                elif isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
                    result[key] = str(value)
                else:
                    result[key] = float(value) if isinstance(value, (int, float)) else value

            # Add some derived insights
            result['trend_signal'] = self._get_trend_signal(latest)
            result['momentum_signal'] = self._get_momentum_signal(latest)

            return result

        except Exception as e:
            raise ValueError(f"Failed to calculate technical indicators: {e}")
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_macd(self, prices: pd.Series, fast=12, slow=26, signal=9) -> Dict[str, pd.Series]:
        """Calculate MACD indicator."""
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal, adjust=False).mean()
        macd_histogram = macd - macd_signal
        return {
            'macd': macd,
            'signal': macd_signal,
            'histogram': macd_histogram
        }

    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: float = 2) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        middle = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }

    def _get_trend_signal(self, latest: pd.Series) -> str:
        """Determine trend based on SMAs."""
        try:
            close = latest.get('Close')
            sma_20 = latest.get('SMA_20')
            sma_50 = latest.get('SMA_50')

            if pd.isna(close) or pd.isna(sma_20):
                return "insufficient_data"

            if close > sma_20 and (pd.isna(sma_50) or sma_20 > sma_50):
                return "bullish"
            elif close < sma_20 and (pd.isna(sma_50) or sma_20 < sma_50):
                return "bearish"
            else:
                return "neutral"
        except Exception:
            return "unknown"

    def _get_momentum_signal(self, latest: pd.Series) -> str:
        """Determine momentum based on RSI."""
        try:
            rsi = latest.get('RSI_14')

            if pd.isna(rsi):
                return "insufficient_data"

            if rsi > 70:
                return "overbought"
            elif rsi < 30:
                return "oversold"
            else:
                return "neutral"
        except Exception:
            return "unknown"

