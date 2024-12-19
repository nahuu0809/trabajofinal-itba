import sqlite3
import logging
from contextlib import contextmanager
from typing import List, Tuple
import pandas as pd

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
            logging.error(f"Error de base de datos: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def setup_database(self):
        """Create necessary tables if they don't exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Crear tabla de datos de acciones
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
                
                # Crear tabla de rangos de fechas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS date_ranges (
                        ticker TEXT PRIMARY KEY,
                        start_date TEXT,
                        end_date TEXT
                    )
                ''')
                
                conn.commit()
                logging.info("Base de datos inicializada correctamente")
                
        except Exception as e:
            logging.error(f"Error al configurar la base de datos: {e}")
            raise

    def save_stock_data(self, ticker: str, data: pd.DataFrame):
        """Save stock data and update date ranges."""
        try:
            with self.get_connection() as conn:
                # Preparar datos para stock_data
                data_to_save = data.copy()
                data_to_save['ticker'] = ticker
                
                # Guardar datos en stock_data
                data_to_save.to_sql('stock_data', conn, if_exists='replace', index=False)
                
                # Actualizar date_ranges
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO date_ranges (ticker, start_date, end_date)
                    VALUES (?, ?, ?)
                ''', (
                    ticker,
                    data['date'].min(),
                    data['date'].max()
                ))
                
                conn.commit()
                logging.info(f"Datos guardados para {ticker}")
                
        except Exception as e:
            logging.error(f"Error al guardar datos: {e}")
            raise

    def get_stock_data(self, ticker: str) -> pd.DataFrame:
        """Get stock data for a specific ticker."""
        try:
            with self.get_connection() as conn:
                query = "SELECT * FROM stock_data WHERE ticker = ? ORDER BY date"
                data = pd.read_sql_query(query, conn, params=(ticker,))
                return data if not data.empty else None
                
        except Exception as e:
            logging.error(f"Error al obtener datos de stock: {e}")
            raise

    def get_stored_stocks(self) -> List[Tuple[str, str, str]]:
        """Get list of stored stocks with their date ranges."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT ticker, start_date, end_date
                    FROM date_ranges
                    ORDER BY ticker
                ''')
                return cursor.fetchall()
                
        except Exception as e:
            logging.error(f"Error al obtener stocks almacenados: {e}")
            raise

    def delete_stock_data(self, ticker: str):
        """Delete all data for a specific ticker."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM stock_data WHERE ticker = ?", (ticker,))
                cursor.execute("DELETE FROM date_ranges WHERE ticker = ?", (ticker,))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error al eliminar datos: {e}")
            raise