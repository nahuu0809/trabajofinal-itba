# ui_utils.py
import tkinter as tk
from tkinter import ttk
import json
import logging

class UIManager:
    def __init__(self, root):
        self.root = root
        
        # Progress bar
        self.progress_frame = ttk.Frame(root)
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=200
        )
        self.progress_label = ttk.Label(self.progress_frame, text="")
        
    def setup_ui(self):
        self.setup_progress_bar()
    
    def setup_progress_bar(self):
        self.progress_frame.pack(side='bottom', fill='x', padx=10, pady=5)
        self.progress_bar.pack(side='right', padx=5)
        self.progress_label.pack(side='right', padx=5)
        
    def show_progress(self, value, text=""):
        self.progress_bar['value'] = value
        self.progress_label['text'] = text
        self.root.update_idletasks()
        
    def hide_progress(self):
        self.progress_frame.pack_forget()