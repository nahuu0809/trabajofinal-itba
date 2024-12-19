import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import pandas as pd
import logging

class StockGraph(ttk.Frame):
    def __init__(self, parent, ticker: str, data: pd.DataFrame):
        super().__init__(parent)
        self.ticker = ticker
        self.data = data
        self.show_menu = None
        self.setup_graph()

    def setup_graph(self):
        try:
            # Create figure
            self.figure = plt.figure(figsize=(10, 6))
            self.ax = self.figure.add_subplot(111)

            # Plot data
            self.ax.plot(self.data['date'], self.data['close'], label='Precio de cierre')
            
            # Customize graph
            self.ax.set_title(f'Precio histórico de {self.ticker}')
            self.ax.set_xlabel('Fecha')
            self.ax.set_ylabel('Precio')
            self.ax.grid(True)
            self.ax.legend()

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            
            # Adjust layout
            plt.tight_layout()

            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.figure, master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Add back button
            ttk.Button(self, text="Volver", command=lambda: self.show_menu() if self.show_menu else None).pack(pady=10)

        except Exception as e:
            logging.error(f"Error al crear el gráfico: {e}")
            raise

    def clear(self):
        plt.close(self.figure)