import tkinter as tk
from tkinter import messagebox
from api_handler import get_stock_data

# Función para manejar el envío de los datos de la API (ejemplo)
def submit_data():
        ticker = ticker_entry.get()
        start_date = date_range_entryFrom.get()
        end_date = date_range_entryTo.get()
        try:
                data = get_stock_data(ticker, start_date, end_date)
                print(data)  # Aquí puedes mostrar los datos de la API o hacer algo con ellos
                tk.messagebox.showinfo("Data", f"Datos recibidos para {ticker}")
        except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")


# Menú de selección de ticker
ticker_label = tk.Label(root, text="Introduzca un Ticker (Por ejemplo Apple = AAPL):")
ticker_entry = tk.Entry(root)

# Rango de fechas
date_range_labelFrom = tk.Label(root, text="Introduce el rango de fechas (Desde):")
date_range_entryFrom = tk.Entry(root, fg="grey")
date_range_entryFrom.insert(0, "YYYY-MM-DD")
date_range_labelTo = tk.Label(root, text="Introduce el rango de fechas (Hasta):")
date_range_entryTo = tk.Entry(root, fg="grey")
date_range_entryTo.insert(0, "YYYY-MM-DD")

# Botón para enviar los datos del ticker y rango de fechas
submit_data_button = tk.Button(root, text="Obtener datos", command=submit_data)