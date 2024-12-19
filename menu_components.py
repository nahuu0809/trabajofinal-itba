import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pandas as pd
from typing import Callable

class MainMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_menu()

    def setup_menu(self):
        # Container frame
        menu_frame = ttk.Frame(self)
        menu_frame.pack(expand=True)

        # Title
        ttk.Label(
            menu_frame, 
            text="Stock Data Application", 
            font=('Arial', 14)
        ).pack(pady=20)

        # Main buttons
        ttk.Button(
            menu_frame,
            text="1. Actualización de datos",
            command=self.show_data_update
        ).pack(pady=10)

        ttk.Button(
            menu_frame,
            text="2. Visualización de datos",
            command=self.show_data_viz
        ).pack(pady=10)

class DataUpdateForm(ttk.Frame):
    def __init__(self, parent, api_handler, db_handler):
        super().__init__(parent)
        self.api_handler = api_handler
        self.db_handler = db_handler
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
            command=self.show_menu
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

            # Fetch data from API with smart update
            data = self.api_handler.get_stock_data_smart_update(ticker, start_date, end_date)
            
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

    def show_menu(self):
        # Implementation depends on your navigation setup
        pass

class DataVisualization(ttk.Frame):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.db_handler = db_handler
        self.setup_visualization()

    def setup_visualization(self):
        # Container
        viz_frame = ttk.Frame(self)
        viz_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Buttons for different views
        ttk.Button(
            viz_frame,
            text="a. Resumen",
            command=self.show_summary
        ).pack(pady=10)

        ttk.Button(
            viz_frame,
            text="b. Gráfico de ticker",
            command=self.show_graph
        ).pack(pady=10)

        # Results area
        self.results_text = tk.Text(viz_frame, height=10, width=50)
        self.results_text.pack(pady=10)

    def show_summary(self):
        """Show summary of stored data"""
        stored_stocks = self.db_handler.get_stored_stocks()
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Los tickers guardados en la base de datos son:\n\n")
        
        for ticker, start_date, end_date in stored_stocks:
            self.results_text.insert(tk.END, 
                f"{ticker} - {start_date} <-> {end_date}\n")

    def show_graph(self):
        """Show graph input dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Gráfico de Ticker")
        
        ttk.Label(dialog, text="Ingrese el ticker a graficar:").pack(pady=5)
        ticker_entry = ttk.Entry(dialog)
        ticker_entry.pack(pady=5)
        
        ttk.Button(
            dialog,
            text="Graficar",
            command=lambda: self.plot_ticker(ticker_entry.get())
        ).pack(pady=10)