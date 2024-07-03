import tkinter as tk
from tkinter import Toplevel, Label, Scale, Button, Entry, messagebox

class InsertarDatosWindow:
    def __init__(self, parent, open_generar_instancias_window):
        self.window = Toplevel(parent)
        self.window.title("Insertar Datos")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        self.open_generar_instancias_window = open_generar_instancias_window

        # Texto "Items"
        self.label_items = Label(self.window, text="Items", font=("Arial", 14))
        self.label_items.pack(pady=10)

        # Slider del 2 al 8
        self.slider = Scale(self.window, from_=2, to=8, orient=tk.HORIZONTAL, font=("Arial", 12))
        self.slider.pack(pady=10)

        # Texto "Cantidad de instancias"
        self.label_instances = Label(self.window, text="Cantidad de instancias", font=("Arial", 14))
        self.label_instances.pack(pady=10)

        # Campo de texto para ingresar cantidad de instancias
        self.cantidad_var = tk.StringVar()
        self.cantidad_entry = Entry(self.window, textvariable=self.cantidad_var, font=("Arial", 12))
        self.cantidad_entry.pack(pady=10)

        # Validación para aceptar solo números mayores de 0
        self.cantidad_entry.config(validate="key", validatecommand=(self.window.register(self.validate_positive_integer), '%P'))

        # Botón "Cargar Datos"
        self.load_button = Button(self.window, text="Cargar Datos", font=("Arial", 12), command=self.load_data)
        self.load_button.pack(pady=10)

    def validate_positive_integer(self, value_if_allowed):
        if value_if_allowed.isdigit() and int(value_if_allowed) > 0:
            return True
        elif value_if_allowed == "":
            return True
        else:
            return False

    def load_data(self):
        columns = self.slider.get()
        try:
            rows = int(self.cantidad_var.get())
            self.open_generar_instancias_window(columns, rows)
        except ValueError:
            messagebox.showerror("Entrada no válida", "Por favor, ingrese un número válido de instancias.")
