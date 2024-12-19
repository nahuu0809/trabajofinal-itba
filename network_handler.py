import requests
import time
import logging
from typing import Callable
import tkinter as tk
from tkinter import ttk

class NetworkHandler:
    def __init__(self, root, api_handler):
        self.root = root
        self.api_handler = api_handler
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.setup_status_indicator()

    def setup_status_indicator(self):
        """Create a network status indicator in the UI."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side='bottom', fill='x', padx=5, pady=2)

        # Create canvas for status dot
        self.canvas = tk.Canvas(
            self.status_frame,
            width=10,
            height=10,
            bg=self.root['bg']
        )
        self.canvas.pack(side='left', padx=5)

        # Create status dot
        self.status_dot = self.canvas.create_oval(2, 2, 8, 8, fill='gray')

        # Status label
        self.status_label = ttk.Label(self.status_frame, text="Checking connection...")
        self.status_label.pack(side='left')

    def update_status_indicator(self, connected: bool):
        """Update the visual status indicator."""
        color = 'green' if connected else 'red'
        text = "Connected" if connected else "Disconnected"
        
        self.canvas.itemconfig(self.status_dot, fill=color)
        self.status_label.config(text=text)

    def execute_with_retry(self, operation: Callable, *args, **kwargs):
        """Execute an API operation with retry logic."""
        retries = 0
        while retries < self.max_retries:
            try:
                result = operation(*args, **kwargs)
                self.update_status_indicator(True)
                return result
            except requests.exceptions.RequestException as e:
                retries += 1
                logging.warning(f"Network error (attempt {retries}/{self.max_retries}): {e}")
                self.update_status_indicator(False)
                
                if retries < self.max_retries:
                    self.status_label.config(text=f"Retrying in {self.retry_delay}s...")
                    self.root.update()
                    time.sleep(self.retry_delay)
                else:
                    raise Exception("Network error: Maximum retries reached")

    def check_connection(self) -> bool:
        """Check API connection status."""
        try:
            self.api_handler.test_connection()
            self.update_status_indicator(True)
            return True
        except:
            self.update_status_indicator(False)
            return False
