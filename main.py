import tkinter as tk
from tkinter import ttk, messagebox
import logging
from ui_utils import UIManager
from api_handler import APIHandler
from db_handler import StockDatabase
from graph_visual import StockGraph
import pandas as pd
from datetime import datetime
from login import LoginWindow
from network_handler import NetworkHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='stock_app.log'
)

class StockApp:
    def __init__(self, root, username):
        try:
            self.root = root
            self.username = username
            self.root.title(f"Stock Data Application - Welcome {username}")
            self.root.geometry("800x600")
            
            # Set up proper window closing
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Initialize components
            self.ui_manager = UIManager(root)
            self.api_handler = APIHandler()
            self.db = StockDatabase()
            self.graph = None
            self.network_handler = NetworkHandler(root, self.api_handler)
            
            # Check initial connection
            self.network_handler.check_connection()
            
            # Setup periodic connection checking
            self.root.after(30000, self.check_connection_periodic)
            
            self.setup_application()
        except Exception as e:
            logging.error(f"Failed to initialize application: {e}")
            messagebox.showerror("Error", "Failed to start application")

    def setup_application(self):
        # Add welcome label
        welcome_frame = ttk.Frame(self.root)
        welcome_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(
            welcome_frame,
            text=f"Welcome, {self.username}!",
            font=('Arial', 12, 'bold')
        ).pack(side='left')

        # Setup UI
        self.ui_manager.setup_ui()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.search_frame = self.create_search_tab()
        self.view_frame = self.create_view_tab()
        self.favorites_frame = self.create_favorites_tab()
        
        # Add tabs to notebook
        self.notebook.add(self.search_frame, text='Search')
        self.notebook.add(self.view_frame, text='View')
        self.notebook.add(self.favorites_frame, text='Favorites')
        
        # Check API connection
        self.check_api_connection()

    def create_search_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # Search components
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text="Ticker:").pack(side='left')
        self.ticker_entry = ttk.Entry(search_frame)
        self.ticker_entry.pack(side='left', padx=5)
        
        ttk.Button(
            search_frame, 
            text="Search", 
            command=self.search_stock
        ).pack(side='left')
        
        # Results area
        self.results_frame = ttk.Frame(frame)
        self.results_frame.pack(fill='both', expand=True)
        
        return frame

    def create_view_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # Stored stocks display
        self.stored_stocks = ttk.Treeview(
            frame,
            columns=('Ticker', 'Last Updated'),
            show='headings'
        )
        self.stored_stocks.heading('Ticker', text='Ticker')
        self.stored_stocks.heading('Last Updated', text='Last Updated')
        self.stored_stocks.pack(fill='both', expand=True)
        
        # Refresh button
        ttk.Button(
            frame,
            text="Refresh",
            command=self.refresh_stored_stocks
        ).pack(pady=5)
        
        return frame

    def create_favorites_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # Favorites list
        self.favorites_list = ttk.Treeview(
            frame,
            columns=('Ticker', 'Added Date'),
            show='headings'
        )
        self.favorites_list.heading('Ticker', text='Ticker')
        self.favorites_list.heading('Added Date', text='Added Date')
        self.favorites_list.pack(fill='both', expand=True)
        
        # Add/Remove buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(
            button_frame,
            text="Add to Favorites",
            command=self.add_to_favorites
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="Remove from Favorites",
            command=self.remove_from_favorites
        ).pack(side='left')
        
        return frame

    def search_stock(self):
        ticker = self.ticker_entry.get().strip().upper()
        if not ticker:
            messagebox.showwarning("Warning", "Please enter a ticker symbol")
            return
            
        try:
            self.ui_manager.show_progress(0, "Fetching data...")
            stock_data = self.fetch_stock_data(ticker, datetime.now(), datetime.now())
            
            if stock_data is not None:
                self.db.save_stock_data(ticker, stock_data)
                self.display_stock_data(ticker, stock_data)
                self.ui_manager.show_progress(100, "Data retrieved successfully")
            else:
                messagebox.showwarning("Warning", "No data found for this ticker")
                
        except Exception as e:
            logging.error(f"Error searching stock {ticker}: {e}")
            messagebox.showerror("Error", f"Failed to fetch stock data: {str(e)}")
        finally:
            self.ui_manager.hide_progress()

    def display_stock_data(self, ticker, data):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Create new graph
        self.graph = StockGraph(self.results_frame, ticker, data)
        self.graph.pack(fill='both', expand=True)

    def refresh_stored_stocks(self):
        try:
            stocks = self.db.get_stored_stocks()
            
            # Clear current display
            for item in self.stored_stocks.get_children():
                self.stored_stocks.delete(item)
                
            # Add stocks to display
            for stock in stocks:
                self.stored_stocks.insert('', 'end', values=stock)
                
        except Exception as e:
            logging.error(f"Error refreshing stored stocks: {e}")
            messagebox.showerror("Error", "Failed to refresh stored stocks")

    def add_to_favorites(self):
        selected = self.stored_stocks.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a stock to add to favorites")
            return
            
        ticker = self.stored_stocks.item(selected[0])['values'][0]
        self.db.add_to_favorites(ticker)
        self.refresh_favorites()

    def remove_from_favorites(self):
        selected = self.favorites_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a stock to remove from favorites")
            return
            
        ticker = self.favorites_list.item(selected[0])['values'][0]
        self.db.remove_from_favorites(ticker)
        self.refresh_favorites()

    def refresh_favorites(self):
        try:
            favorites = self.db.get_favorites()
            
            # Clear current display
            for item in self.favorites_list.get_children():
                self.favorites_list.delete(item)
                
            # Add favorites to display
            for favorite in favorites:
                self.favorites_list.insert('', 'end', values=favorite)
                
        except Exception as e:
            logging.error(f"Error refreshing favorites: {e}")
            messagebox.showerror("Error", "Failed to refresh favorites")

    def check_api_connection(self):
        if not self.api_handler.test_connection():
            messagebox.showwarning(
                "API Connection",
                "Could not connect to API. Some features may be limited."
            )

    def on_closing(self):
        """Handle window closing event"""
        try:
            # Clean up resources
            if hasattr(self, 'graph') and self.graph:
                self.graph.clear()
            
            # Destroy the window
            self.root.destroy()
            
            # Ensure the application exits completely
            self.root.quit()
            
        except Exception as e:
            logging.error(f"Error during application shutdown: {e}")
        finally:
            # Force exit if needed
            import sys
            sys.exit(0)

    def check_connection_periodic(self):
        """Periodically check connection status."""
        self.network_handler.check_connection()
        self.root.after(30000, self.check_connection_periodic)
        
    def fetch_stock_data(self, ticker, start_date, end_date):
        """Fetch stock data with retry logic."""
        return self.network_handler.execute_with_retry(
            self.api_handler.get_stock_data,
            ticker, start_date, end_date
        )

if __name__ == "__main__":
    try:
        # Show login window first
        login = LoginWindow()
        username = login.show()
        
        if username:
            # Start main application
            root = tk.Tk()
            app = StockApp(root, username)
            root.mainloop()
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Error", "An error occurred while starting the application")
    finally:
        # Ensure complete exit
        import sys
        sys.exit(0)