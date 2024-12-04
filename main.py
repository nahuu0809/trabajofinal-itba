import tkinter as tk
from tkinter import messagebox
from api_handler import get_stock_data
from res_info import submit_data

def about():
    messagebox.showinfo(title="About Us", message="Proyecto Final Python en ITBA by Nahuel Diaz")

def on_submit():
    username = entry.get()
    messagebox.showinfo(title= "", message= f"Bienvenido, {username}")

    # Cambiar la interfaz para mostrar el usuario logueado
    #logged_in_label.config(text=f"Usuario logeado: {username}")
    root.title(f"Trabajo Final Python - Usuario logeado: {username}")
    
    # Hacer visibles los componentes del menú para seleccionar el ticker y el rango de fechas
    ticker_label.pack(fill="both" , expand=True)
    ticker_entry.pack(pady=5, expand=True)
    date_range_labelFrom.pack(fill="both", expand=True)
    date_range_entryFrom.pack(pady=5, expand=True)
    date_range_labelTo.pack(fill="both", expand=True)
    date_range_entryTo.pack(pady=5, expand=True)
    submit_data_button.pack(pady=5, expand=True)
    
    # Hacer desaparecer el campo de entrada y el botón de enviar
    label.pack_forget()
    entry.pack_forget()
    submit_button.pack_forget()
    
def on_res():
    submit_data()

# Crear ventana principal
root = tk.Tk()
root.title("Aplicación con Interfaz")
root.geometry("480x320")

#Crear Menu
menu = tk.Menu(root)
root.config(menu=menu)

# Crear un submenú
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Menu", menu=file_menu)
file_menu.add_cascade(label="Acerca de", command=about)
file_menu.add_command(label="Salir", command=root.quit)

# Etiqueta
label = tk.Label(root, text="Introduce tu nombre:")
label.pack(pady=30, fill="x", expand=True)

# Label para mostrar el estado de usuario logeado
logged_in_label = tk.Label(root, text="")
logged_in_label.pack(pady=30, fill="x", expand=True)

# Entrada de texto
entry = tk.Entry(root)
entry.pack(pady=30, expand=True)

# Botón de envío
submit_button = tk.Button(root, text="Enviar", command=on_submit)
submit_button.pack(pady=30, expand=True)

#Boton Menu Resumen
res_btn = tk.Button(root, text="Resumen de datos guardados", command=on_submit)
res_btn.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.mainloop()