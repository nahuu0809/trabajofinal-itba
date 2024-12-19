import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self):
        self.username = None
        self.root = tk.Tk()
        self.root.title("Stock App Login")
        self.root.geometry("800x600")
        
        # Set up proper window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_login_ui()

    def setup_login_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            main_frame, 
            text="Stock Data Application", 
            font=('Arial', 14, 'bold')
        ).pack(pady=10)

        # Username entry
        ttk.Label(main_frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(pady=5)

        # Login button
        ttk.Button(
            main_frame, 
            text="Login", 
            command=self.login
        ).pack(pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        if username:
            self.username = username
            self.root.quit()
        else:
            messagebox.showerror("Error", "Please enter a username")

    def show(self):
        self.root.mainloop()
        self.root.destroy()
        return self.username

    def on_closing(self):
        """Handle window closing event"""
        self.root.quit()
        self.root.destroy()
        import sys
        sys.exit(0)