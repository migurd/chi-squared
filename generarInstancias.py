import tkinter as tk
from tkinter import Toplevel, Frame, Button, Entry, Checkbutton, Label, Scrollbar, Canvas

class GenerarInstanciasWindow:
    def __init__(self, parent, columns, rows):
        self.window = Toplevel(parent)
        self.window.title("Generar Instancias")
        self.window.geometry("800x600")

        # Número de columnas y filas
        self.columns = columns
        self.rows = rows

        # Crear marco para los checkbuttons
        self.checkbutton_frame = Frame(self.window)
        self.checkbutton_frame.pack(pady=10, fill=tk.X)

        # Crear numeración y checkbuttons para columnas
        self.check_vars = []  # Lista para almacenar las variables de los checkbuttons
        self.check_vars_labels = []  # Lista para almacenar los labels con numeración

        self.selected_checkbuttons = []  # Lista para almacenar los checkbuttons seleccionados

        for j in range(self.columns):
            var = tk.BooleanVar()
            var.trace_add("write", self.check_limit)  # Añadir el rastreador para la variable
            self.check_vars.append(var)
            label = Label(self.checkbutton_frame, text=f"Item {j + 1}", font=("Arial", 12, "bold"))
            label.grid(row=0, column=j*2, padx=5)
            checkbutton = Checkbutton(self.checkbutton_frame, variable=var, onvalue=True, offvalue=False)
            checkbutton.grid(row=0, column=j*2 + 1, padx=5)

        # Crear marco para la tabla
        self.table_frame = Frame(self.window)
        self.table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Crear canvas y scrollbar
        self.canvas = Canvas(self.table_frame)
        self.scroll_y = Scrollbar(self.table_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.table = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table, anchor="nw")

        self.populate_table()

        # Botones
        self.button_frame = Frame(self.window)
        self.button_frame.pack(pady=20)

        self.generate_button = Button(self.button_frame, text="Generar Instancias al Azar", command=self.generate_random_instances)
        self.generate_button.pack(pady=5, fill=tk.X)

        self.clear_button = Button(self.button_frame, text="Limpiar", command=self.clear_table)
        self.clear_button.pack(pady=5, fill=tk.X)

        self.results_button = Button(self.button_frame, text="Obtener Resultados", command=self.get_results)
        self.results_button.pack(pady=5, fill=tk.X)

        # Actualizar el área del canvas
        self.table.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def check_limit(self, *args):
        # Contar el número de checkbuttons marcados
        marked_count = sum(var.get() for var in self.check_vars)

        if marked_count > 2:
            # Desmarcar el último checkbutton marcado
            for var in reversed(self.check_vars):
                if var.get():
                    var.set(False)
                    break

    def populate_table(self):
        # Limpiar tabla existente
        for widget in self.table.winfo_children():
            widget.destroy()
        self.entries = []  # Lista para almacenar las entradas de la tabla

        # Crear entradas de la tabla
        self.entries = []  # Inicializar la lista de entradas
        for i in range(self.rows):
            row_entries = []  # Lista para las entradas en la fila actual
            for j in range(self.columns):
                entry = tk.Entry(self.table, width=10, font=("Arial", 12), justify="center", relief="solid")
                entry.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                row_entries.append(entry)
            self.entries.append(row_entries)  # Agregar las entradas de la fila a la lista

        # Configurar el ancho de las columnas y el alto de las filas
        for j in range(self.columns):
            self.table.columnconfigure(j, weight=1, minsize=80)
        for i in range(self.rows):
            self.table.rowconfigure(i, weight=1, minsize=30)

    def clear_table(self):
        # Limpiar solo los datos de las entradas, sin eliminar la estructura de la tabla
        for row_entries in self.entries:
            for entry in row_entries:
                entry.delete(0, tk.END)

    def generate_random_instances(self):
        # Implementar lógica para generar instancias al azar
        pass

    def get_results(self):
        # Implementar lógica para obtener resultados
        pass
