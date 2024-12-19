import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import pandas as pd
import logging
from typing import Dict, Any
from datetime import datetime
from technical_analysis import TechnicalAnalysis

class StockGraph(ttk.Frame):
    def __init__(self, parent, ticker: str, data: pd.DataFrame):
        super().__init__(parent)
        self.ticker = ticker
        self.data = data
        self.setup_graph()

    def setup_graph(self):
        """Initialize and setup the graph components."""
        try:
            # Create figure with price and volume subplots
            self.figure = plt.figure(figsize=(10, 6), facecolor='white')
            gs = self.figure.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.1)
            self.price_ax = self.figure.add_subplot(gs[0])
            self.volume_ax = self.figure.add_subplot(gs[1], sharex=self.price_ax)

            # Style configuration
            plt.style.use('classic')
            self.price_ax.grid(True, linestyle='--', alpha=0.7)
            self.volume_ax.grid(True, linestyle='--', alpha=0.7)

            # Plot data
            self.plot_price_data()
            self.plot_volume_data()

            # Create header with stock info
            self.create_header()

            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.figure, master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Add trading info
            self.add_trading_info()

        except Exception as e:
            logging.error(f"Error setting up graph: {e}")
            raise

    def create_header(self):
        """Create header with stock information."""
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        # Current price and change
        current_price = self.data['close'].iloc[-1]
        price_change = self.data['close'].iloc[-1] - self.data['close'].iloc[-2]
        price_change_pct = (price_change / self.data['close'].iloc[-2]) * 100

        # Left side - Ticker and Price
        left_frame = ttk.Frame(header_frame)
        left_frame.pack(side=tk.LEFT)

        ttk.Label(
            left_frame, 
            text=self.ticker, 
            font=('Arial', 24, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        price_color = 'green' if price_change >= 0 else 'red'
        ttk.Label(
            left_frame,
            text=f"${current_price:.2f}",
            font=('Arial', 20)
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(
            left_frame,
            text=f"{price_change:+.2f} ({price_change_pct:+.2f}%)",
            font=('Arial', 16),
            foreground=price_color
        ).pack(side=tk.LEFT, padx=5)

    def add_trading_info(self):
        """Add trading information panel."""
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        # Calculate trading info
        high = self.data['high'].max()
        low = self.data['low'].min()
        volume = self.data['volume'].iloc[-1]
        avg_volume = self.data['volume'].mean()

        # Create info labels
        info_items = [
            ('Day Range', f"${low:.2f} - ${high:.2f}"),
            ('Volume', f"{volume:,.0f}"),
            ('Avg Volume', f"{avg_volume:,.0f}"),
        ]

        for label, value in info_items:
            item_frame = ttk.Frame(info_frame)
            item_frame.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(
                item_frame,
                text=label,
                font=('Arial', 10, 'bold')
            ).pack(anchor='w')
            
            ttk.Label(
                item_frame,
                text=value,
                font=('Arial', 10)
            ).pack(anchor='w')

    def plot_price_data(self):
        """Plot the price data."""
        try:
            # Original price plot
            self.price_ax.plot(self.data['date'], self.data['close'], color='#0066cc', linewidth=1.5, label='Price')
            
            # Calculate and plot technical indicators
            indicators = TechnicalAnalysis.calculate_indicators(self.data)
            
            # Plot Bollinger Bands
            bb = indicators['BB']
            self.price_ax.plot(self.data['date'], bb['upper'], 'r--', alpha=0.3, label='BB Upper')
            self.price_ax.plot(self.data['date'], bb['middle'], 'g--', alpha=0.3, label='BB Middle')
            self.price_ax.plot(self.data['date'], bb['lower'], 'r--', alpha=0.3, label='BB Lower')
            
            # Add RSI subplot
            self.rsi_ax = self.figure.add_subplot(gs[2], sharex=self.price_ax)
            self.rsi_ax.plot(self.data['date'], indicators['RSI'], color='purple', label='RSI')
            self.rsi_ax.axhline(y=70, color='r', linestyle='--', alpha=0.3)
            self.rsi_ax.axhline(y=30, color='g', linestyle='--', alpha=0.3)
            self.rsi_ax.set_ylabel('RSI')
            
            # Update legend and labels
            self.price_ax.legend(loc='upper left')
            self.rsi_ax.legend(loc='upper right')
            
        except Exception as e:
            logging.error(f"Error plotting technical indicators: {e}")
            raise

    def plot_volume_data(self):
        """Plot the volume data."""
        try:
            # Plot volume bars
            self.volume_ax.bar(self.data['date'], self.data['volume'], color='#999999', alpha=0.5)
            
            self.volume_ax.set_ylabel("Volume")
            self.volume_ax.set_xlabel("Date")
            
            # Format y-axis to show volume in millions/thousands
            self.volume_ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M' if x >= 1e6 
                                else f'{x/1e3:.1f}K'))

        except Exception as e:
            logging.error(f"Error plotting volume data: {e}")
            raise

    def update_data(self, new_data: Dict[str, Any]):
        """Update the graph with new data."""
        try:
            # Append new data point
            new_row = pd.DataFrame([{
                'date': new_data['timestamp'],
                'close': new_data['price'],
                'volume': new_data['volume']
            }])
            
            self.data = pd.concat([self.data, new_row])
            
            # Keep only last 100 points for performance
            if len(self.data) > 100:
                self.data = self.data.iloc[-100:]

            # Clear and redraw
            self.figure.clear()
            self.setup_graph()
            self.canvas.draw()

        except Exception as e:
            logging.error(f"Error updating graph: {e}")
            raise

    def clear(self):
        """Clear the graph."""
        plt.close(self.figure)