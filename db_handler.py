import sqlite3
import logging
from contextlib import contextmanager
from typing import List, Tuple, Optional
import pandas as pd
from datetime import datetime

class StockDatabase:
    def __init__(self, db_file: str = 'stocks.db'):
        self.db_file = db_file
        self.setup_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            yield conn
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def setup_database(self):
        """Create necessary tables if they don't exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Stock data table only
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stock_data (
                        ticker TEXT,
                        date TEXT,
                        open REAL,
                        high REAL,
                        low REAL,
                        close REAL,
                        volume INTEGER,
                        PRIMARY KEY (ticker, date)
                    )
                ''')
                
                conn.commit()
                
        except Exception as e:
            logging.error(f"Failed to setup database: {e}")
            raise

    def save_stock_data(self, ticker: str, data: pd.DataFrame):
        """Save stock data to database with date tracking."""
        try:
            with self.get_connection() as conn:
                # Convert DataFrame to SQL-friendly format
                data['ticker'] = ticker
                
                # Use INSERT OR REPLACE to handle updates
                data.to_sql('stock_data', conn, if_exists='replace', index=False)
                
                # Update date range tracking
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO date_ranges 
                    (ticker, start_date, end_date) 
                    VALUES (?, ?, ?)
                ''', (
                    ticker,
                    data['date'].min(),
                    data['date'].max()
                ))
                
                conn.commit()
                logging.info(f"Saved data for {ticker}")
                
        except Exception as e:
            logging.error(f"Failed to save stock data: {e}")
            raise

    def get_stored_stocks(self) -> List[Tuple[str, str, str]]:
        """Get list of stored stocks with their date ranges."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        ticker,
                        MIN(date) as start_date,
                        MAX(date) as end_date
                    FROM stock_data
                    GROUP BY ticker
                    ORDER BY ticker
                ''')
                return cursor.fetchall()
                
        except Exception as e:
            logging.error(f"Failed to get stored stocks: {e}")
            raise

    def get_stock_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """Retrieve stock data from database."""
        try:
            with self.get_connection() as conn:
                query = "SELECT * FROM stock_data WHERE ticker = ? ORDER BY date"
                return pd.read_sql_query(query, conn, params=(ticker,))
                
        except Exception as e:
            logging.error(f"Failed to get stock data: {e}")
            return None

    def add_to_favorites(self, ticker: str):
        """Add stock to favorites."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO favorites (ticker, added_date) VALUES (?, ?)",
                    (ticker, datetime.now().strftime('%Y-%m-%d'))
                )
                conn.commit()
                
        except Exception as e:
            logging.error(f"Failed to add favorite: {e}")
            raise

    def remove_from_favorites(self, ticker: str):
        """Remove stock from favorites."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM favorites WHERE ticker = ?", (ticker,))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Failed to remove favorite: {e}")
            raise

    def get_favorites(self) -> List[Tuple[str, str]]:
        """Get list of favorite stocks."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ticker, added_date FROM favorites ORDER BY added_date DESC")
                return cursor.fetchall()
                
        except Exception as e:
            logging.error(f"Failed to get favorites: {e}")
            raise