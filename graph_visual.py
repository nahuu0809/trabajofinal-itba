import matplotlib.pyplot as plt
import pandas as pd

def plot_stock_data(ticker, data):
    df = pd.DataFrame(data, columns=['Date', 'Close'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'])
    plt.title(f'Precio de cierre de {ticker}')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de cierre')
    plt.grid(True)
    plt.show()