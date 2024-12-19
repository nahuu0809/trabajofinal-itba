import pandas as pd
import numpy as np
from typing import Dict

class TechnicalAnalysis:
    @staticmethod
    def calculate_indicators(data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate technical indicators for the given data."""
        indicators = {}
        
        # RSI (Relative Strength Index)
        indicators['RSI'] = TechnicalAnalysis.calculate_rsi(data['close'])
        
        # MACD (Moving Average Convergence Divergence)
        indicators['MACD'] = TechnicalAnalysis.calculate_macd(data['close'])
        
        # Bollinger Bands
        indicators['BB'] = TechnicalAnalysis.calculate_bollinger_bands(data['close'])
        
        return indicators

    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI technical indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def calculate_macd(prices: pd.Series) -> Dict[str, pd.Series]:
        """Calculate MACD indicator."""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        
        return {
            'macd': macd,
            'signal': signal,
            'histogram': macd - signal
        }

    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        return {
            'upper': sma + (std * 2),
            'middle': sma,
            'lower': sma - (std * 2)
        }
