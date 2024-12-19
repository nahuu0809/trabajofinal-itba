import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pandas as pd

class MainMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.show_data_update = None
        self.show_data_viz = None
        self.setup_menu()

    def setup_menu(self):
        # Container frame
        menu_frame = ttk.Frame(self)
        menu_frame.pack(expand=True)

        # Title
        ttk.Label(
            menu_frame, 
            text="Aplicación de Datos Bursátiles", 
            font=('Arial', 14)
        ).pack(pady=20)

        # Main buttons
        ttk.Button(
            menu_frame,
            text="1. Actualización de datos",
            command=lambda: self.show_data_update() if self.show_data_update else None
        ).pack(pady=10)

        ttk.Button(
            menu_frame,
            text="2. Visualización de datos",
            command=lambda: self.show_data_viz() if self.show_data_viz else None
        ).pack(pady=10)

class DataUpdateForm(ttk.Frame):
    def __init__(self, parent, api_handler, db_handler):
        super().__init__(parent)
        self.api_handler = api_handler
        self.db_handler = db_handler
        self.show_menu = None
        self.setup_form()

    def setup_form(self):
        # Form container
        form_frame = ttk.LabelFrame(self, text="Actualización de datos", padding="20")
        form_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Ticker input
        ttk.Label(form_frame, text="Ingrese ticker:").pack(anchor='w', pady=5)
        self.ticker_entry = ttk.Entry(form_frame)
        self.ticker_entry.pack(fill='x', pady=5)

        # Date inputs
        ttk.Label(form_frame, text="Fecha inicio (YYYY/MM/DD):").pack(anchor='w', pady=5)
        self.start_date = ttk.Entry(form_frame)
        self.start_date.pack(fill='x', pady=5)

        ttk.Label(form_frame, text="Fecha fin (YYYY/MM/DD):").pack(anchor='w', pady=5)
        self.end_date = ttk.Entry(form_frame)
        self.end_date.pack(fill='x', pady=5)

        # Action buttons
        ttk.Button(
            form_frame,
            text="Guardar datos",
            command=self.save_to_database
        ).pack(pady=10)

        ttk.Button(
            form_frame,
            text="Volver al menú",
            command=lambda: self.show_menu() if self.show_menu else None
        ).pack(pady=5)

        # Status label
        self.status_label = ttk.Label(form_frame, text="")
        self.status_label.pack(pady=10)

    def save_to_database(self):
        """Save stock data to database."""
        ticker = self.ticker_entry.get().strip().upper()
        start_date = self.start_date.get().strip()
        end_date = self.end_date.get().strip()

        if not all([ticker, start_date, end_date]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        try:
            self.status_label.config(text="Pidiendo datos...")
            self.update()

            # Fetch data from API
            data = self.api_handler.get_stock_data(ticker, start_date, end_date)
            
            if data is not None:
                # Save to database
                self.db_handler.save_stock_data(ticker, data)
                self.status_label.config(text="Datos guardados correctamente")
                messagebox.showinfo("Éxito", "Datos guardados en la base de datos")
            else:
                raise ValueError(f"No hay datos disponibles para {ticker}")

        except Exception as e:
            self.status_label.config(text="Error al guardar datos")
            messagebox.showerror("Error", str(e))

class DataVisualization(ttk.Frame):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.db_handler = db_handler
        self.show_menu = None
        self.setup_visualization()

    def setup_visualization(self):
        # Container principal
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Frame para entrada directa de ticker (ahora arriba)
        ticker_frame = ttk.Frame(main_frame)
        ticker_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(
            ticker_frame,
            text="Ingrese ticker a graficar:"
        ).pack(side='left', padx=5)

        self.ticker_entry = ttk.Entry(ticker_frame, width=10)
        self.ticker_entry.pack(side='left', padx=5)

        ttk.Button(
            ticker_frame,
            text="Graficar",
            command=lambda: self.plot_ticker(self.ticker_entry.get())
        ).pack(side='left', padx=5)

        # Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)

        # Botones alineados horizontalmente
        ttk.Button(
            button_frame,
            text="a. Resumen",
            width=20,
            command=self.show_summary
        ).pack(side='left', padx=5)

        # Área de resultados
        self.results_text = tk.Text(main_frame, height=10, width=50)
        self.results_text.pack(pady=10)

        # Frame para el botón de volver
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill='x', pady=(10, 0))

        ttk.Button(
            bottom_frame,
            text="Volver al menú",
            command=lambda: self.show_menu() if self.show_menu else None
        ).pack(side='right', padx=5)

    def plot_ticker(self, ticker):
        """Plot the ticker data"""
        if not ticker:
            messagebox.showwarning("Error", "Por favor ingrese un ticker")
            return
            
        ticker = ticker.strip().upper()
        try:
            data = self.db_handler.get_stock_data(ticker)
            if data is not None and not data.empty:
                from graph_visual import StockGraph
                graph_window = tk.Toplevel(self)
                graph_window.title(f"Gráfico de {ticker}")
                graph_window.geometry("800x600")
                
                # Crear el gráfico y pasar el show_menu
                graph = StockGraph(graph_window, ticker, data)
                graph.show_menu = self.show_menu  # Agregar esta línea
                graph.pack(expand=True, fill='both')
            else:
                messagebox.showwarning("Error", f"No hay datos disponibles para {ticker}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el gráfico: {str(e)}")

    def show_summary(self):
        """Show summary of stored data"""
        stored_stocks = self.db_handler.get_stored_stocks()
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Los tickers guardados en la base de datos son:\n\n")
        
        for ticker, start_date, end_date in stored_stocks:
            self.results_text.insert(tk.END, 
                f"{ticker} - {start_date} <-> {end_date}\n")