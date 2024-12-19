import tkinter as tk
from tkinter import ttk, messagebox
import os

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplicación de Datos Financieros -Login")
        self.root.geometry("400x300")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Título
        ttk.Label(
            main_frame,
            text="Bienvenido Usuario",
            font=('Arial', 14)
        ).pack(pady=10)
        
        # Username
        ttk.Label(main_frame, text="Ingre su usuario:").pack(pady=5)
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(pady=5)
        
        # Login button
        ttk.Button(
            main_frame,
            text="Ingresar",
            command=self.login
        ).pack(pady=20)
        
        self.username = None
        
        # Manejar el cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def login(self):
        username = self.username_entry.get().strip()
        if username:
            self.username = username
            self.root.quit()
        else:
            messagebox.showerror("Error", "Por favor ingrese un usuario")

    def on_closing(self):
        self.root.destroy()
        os._exit(0)

    def show(self):
        self.root.mainloop()
        return self.username