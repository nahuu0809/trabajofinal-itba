import sqlite3

def create_connection():
    conn = sqlite3.connect('stocks.db')
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    close REAL,
    high REAL,
    low REAL,
    volume INTEGER
    )
''')
    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    # Insertar los datos del ticker en la base de datos
    for data in data:
        cursor.execute('''
        INSERT INTO tickers (ticker, date, open, close, high, low, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['ticker'], data['date'], data['open'], data['close'], data['high'], data['low'], data['volume']))

    conn.commit()
    conn.close()
