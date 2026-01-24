import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd


class MarketDataFetcher:
    """
    Fetch market data from yfinance
    Handles caching and error handling
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize market data fetcher
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def fetch_latest_price(self, symbol: str) -> Decimal:
        """
        Fetch current price for a symbol
        
        Args:
            symbol: Ticker symbol
            
        Returns:
            Current price
        """
        pass
    
    def fetch_historical_prices(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime = None
    ) -> pd.DataFrame:
        """
        Fetch historical price data
        
        Args:
            symbol: Ticker symbol
            start_date: Start date
            end_date: End date (defaults to today)
            
        Returns:
            DataFrame with OHLCV data
        """
        pass
    
    def update_price_history(self, symbol: str) -> int:
        """
        Update price history in database
        
        Args:
            symbol: Ticker symbol
            
        Returns:
            Number of records added
        """
        pass
    
    def bulk_update_prices(self, symbols: List[str]) -> Dict[str, int]:
        """
        Update prices for multiple symbols
        
        Args:
            symbols: List of ticker symbols
            
        Returns:
            Dictionary of symbol -> records added
        """
        pass
    
    def get_asset_info(self, symbol: str) -> Dict:
        """
        Fetch asset metadata from yfinance
        
        Returns sector, industry, company name, etc.
        
        Args:
            symbol: Ticker symbol
            
        Returns:
            Dictionary with asset information
        """
        pass