import tkinter as tk
from tkinter import ttk, messagebox
import logging
from api_handler import APIHandler
from db_handler import StockDatabase
from menu_components import MainMenu, DataUpdateForm, DataVisualization
from login_window import LoginWindow
from dotenv import load_dotenv
import os

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
            
            # Cargar variables .env
            load_dotenv()
            
            # Verificar variables de entorno
            required_env_vars = ['API_KEY', 'BASE_URL_HIS', 'BASE_URL_REAL']
            missing_vars = [var for var in required_env_vars if not os.getenv(var)]
            
            if missing_vars:
                raise ValueError(f"Faltan variables de entorno: {', '.join(missing_vars)}")

            self.root.title(f"Aplicación de Datos Financieros - Usuario Logueado: {username}")
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
            
            # Configurar el manejador de cierre
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
        except Exception as e:
            logging.error(f"Error al inicializar la aplicación: {e}")
            messagebox.showerror("Error", f"Error al inicializar la aplicación: {str(e)}")
            self.on_closing()

    def setup_header(self):
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(header_frame, text=f"Usuario Logueado: {self.username}", font=('Arial', 10)).pack(side='right', padx=10)

    def show_main_menu(self):
        self.clear_container()
        menu = MainMenu(self.main_container)
        menu.show_data_update = self.show_data_update
        menu.show_data_viz = self.show_data_viz
        menu.pack(expand=True, fill='both')

    def show_data_update(self):
        self.clear_container()
        form = DataUpdateForm(self.main_container, self.api_handler, self.db, self.username)
        form.show_menu = self.show_main_menu
        form.pack(expand=True, fill='both')

    def show_data_viz(self):
        self.clear_container()
        viz = DataVisualization(self.main_container, self.db)
        viz.show_menu = self.show_main_menu
        viz.pack(expand=True, fill='both')

    def clear_container(self):
        for widget in list(self.main_container.winfo_children())[1:]:
            widget.destroy()

    def on_closing(self):
        # Manejar el cierre de la aplicación principal
        try:
            if hasattr(self, 'db'):
                # Cerrar conexiones de base de datos si existen
                del self.db
            if hasattr(self, 'api_handler'):
                # Limpiar recursos del API handler si es necesario
                del self.api_handler
            self.root.destroy()
            os._exit(0)
        except Exception as e:
            logging.error(f"Error al cerrar la aplicación: {e}")
            os._exit(1)

def main():
    try:
        login = LoginWindow()
        username = login.show()
        
        if username:
            # Asegurarse de que la ventana de login esté completamente cerrada
            try:
                login.root.destroy()
            except:
                pass
            
            # Iniciar la aplicación principal
            root = tk.Tk()
            app = StockApp(root, username)
            root.mainloop()
    except Exception as e:
        logging.error(f"Error en la aplicación: {e}")
        messagebox.showerror("Error", "Ocurrió un error al iniciar la aplicación")
        os._exit(1)

if __name__ == "__main__":
    main()