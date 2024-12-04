import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables de .env si existe

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"

def get_stock_data(ticker, start_date, end_date):
    url = f"{BASE_URL}/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener datos: {response.status_code}")