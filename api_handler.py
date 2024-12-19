import requests
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()

class APIHandler:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url_his = os.getenv('BASE_URL_HIS')
        self.base_url_real = os.getenv('BASE_URL_REAL')
        
        if not all([self.api_key, self.base_url_his, self.base_url_real]):
            raise ValueError("Missing required environment variables")
            
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def test_connection(self) -> bool:
        """Test the API connection."""
        try:
            response = self.session.get(
                f"{self.base_url_real}?apiKey={self.api_key}",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logging.error(f"API connection test failed: {e}")
            return False

    def get_stock_data(self, ticker: str, start_date: Optional[str] = None, 
                      end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Fetch stock data for a given ticker and date range.
        
        Args:
            ticker: Stock symbol
            start_date: Start date in YYYY/MM/DD format (optional)
            end_date: End date in YYYY/MM/DD format (optional)
            
        Returns:
            DataFrame with stock data or None if request fails
        """
        try:
            # Set default dates if not provided
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

            # Convert date format from YYYY/MM/DD to YYYY-MM-DD
            start_date = start_date.replace('/', '-')
            end_date = end_date.replace('/', '-')

            # Ensure dates are within valid range
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
            if end_datetime > datetime.now():
                end_date = datetime.now().strftime('%Y-%m-%d')

            url = f"{self.base_url_his}/{ticker}/range/1/day/{start_date}/{end_date}"
            params = {"apiKey": self.api_key}
            
            logging.info(f"Requesting data for {ticker} from {start_date} to {end_date}")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'results' not in data:
                logging.warning(f"No data available for {ticker}")
                return None
                
            # Convert to DataFrame
            df = pd.DataFrame(data['results'])
            df['date'] = pd.to_datetime(df['t'], unit='ms').dt.date
            df = df.rename(columns={
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'v': 'volume'
            })
            
            return df[['date', 'open', 'high', 'low', 'close', 'volume']]
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed for {ticker}: {e}")
            raise Exception(f"Failed to fetch data: {str(e)}")
        except Exception as e:
            logging.error(f"Error processing data for {ticker}: {e}")
            raise Exception(f"Error processing data: {str(e)}")

    def get_realtime_quote(self, ticker: str) -> Dict[str, Any]:
        """
        Get real-time quote for a ticker.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            Dictionary with current price data
        """
        try:
            url = f"{self.base_url_real}/{ticker}/last"
            params = {"apiKey": self.api_key}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'price': data.get('last', {}).get('price', 0),
                'timestamp': datetime.now(),
                'volume': data.get('last', {}).get('size', 0)
            }
            
        except Exception as e:
            logging.error(f"Failed to get real-time quote for {ticker}: {e}")
            raise Exception(f"Failed to get quote: {str(e)}")

    def get_company_info(self, ticker: str) -> Dict[str, Any]:
        """
        Get company information for a ticker.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            Dictionary with company information
        """
        try:
            url = f"{self.base_url_real}/{ticker}"
            params = {"apiKey": self.api_key}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get('results', {})
            
        except Exception as e:
            logging.error(f"Failed to get company info for {ticker}: {e}")
            raise Exception(f"Failed to get company info: {str(e)}")

    def __del__(self):
        """Cleanup method to close the session."""
        if hasattr(self, 'session'):
            self.session.close()