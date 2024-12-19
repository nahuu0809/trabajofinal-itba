import tkinter as tk
from tkinter import ttk, messagebox
import logging
from api_handler import APIHandler
from db_handler import StockDatabase
from menu_components import MainMenu, DataUpdateForm, DataVisualization
from dotenv import load_dotenv
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='stock_app.log'
)

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("400x300")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Título
        ttk.Label(
            main_frame,
            text="Bienvenido",
            font=('Arial', 14)
        ).pack(pady=10)
        
        # Username
        ttk.Label(main_frame, text="Usuario:").pack(pady=5)
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
        """Manejar el cierre de la ventana"""
        self.root.quit()
        self.root.destroy()
        import sys
        sys.exit(0)  # Salir limpiamente del programa

    def show(self):
        self.root.mainloop()
        if hasattr(self.root, 'destroy'):  # Verificar si la ventana aún existe
            self.root.destroy()
        return self.username

class StockApp:
    def __init__(self, root, username):
        try:
            # Cargar variables de entorno
            load_dotenv()
            
            # Verificar variables de entorno
            required_env_vars = ['API_KEY', 'BASE_URL_HIS', 'BASE_URL_REAL']
            missing_vars = [var for var in required_env_vars if not os.getenv(var)]
            
            if missing_vars:
                raise ValueError(f"Faltan variables de entorno: {', '.join(missing_vars)}")

            self.root = root
            self.username = username
            self.root.title(f"Aplicación de Datos Bursátiles - Usuario: {username}")
            self.root.geometry("800x600")
            
            # Initialize components
            self.api_handler = APIHandler()
            self.db = StockDatabase()
            
            # Setup main container
            self.main_container = ttk.Frame(root)
            self.main_container.pack(expand=True, fill='both')
            
            # Add username label
            self.setup_header()
            
            # Start with main menu
            self.show_main_menu()
            
        except Exception as e:
            logging.error(f"Error al inicializar la aplicación: {e}")
            messagebox.showerror("Error", f"Error al inicializar la aplicación: {str(e)}")
            raise

    def setup_header(self):
        """Setup header with username"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(
            header_frame,
            text=f"Usuario: {self.username}",
            font=('Arial', 10)
        ).pack(side='right', padx=10)

    def show_main_menu(self):
        self.clear_container()
        menu = MainMenu(self.main_container)
        menu.show_data_update = self.show_data_update
        menu.show_data_viz = self.show_data_viz
        menu.pack(expand=True, fill='both')

    def show_data_update(self):
        self.clear_container()
        form = DataUpdateForm(self.main_container, self.api_handler, self.db)
        form.show_menu = self.show_main_menu
        form.pack(expand=True, fill='both')

    def show_data_viz(self):
        self.clear_container()
        viz = DataVisualization(self.main_container, self.db)
        viz.show_menu = self.show_main_menu
        viz.pack(expand=True, fill='both')

    def clear_container(self):
        """Clear main container except header"""
        for widget in list(self.main_container.winfo_children())[1:]:
            widget.destroy()

if __name__ == "__main__":
    try:
        # Show login window
        login = LoginWindow()
        username = login.show()
        
        if username:  # Solo iniciar la aplicación principal si hay un usuario
            root = tk.Tk()
            app = StockApp(root, username)
            root.mainloop()
    except Exception as e:
        logging.error(f"Error en la aplicación: {e}")
        messagebox.showerror("Error", "Ocurrió un error al iniciar la aplicación")