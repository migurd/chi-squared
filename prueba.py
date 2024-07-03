import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk, ImageDraw
from insertarDatos import InsertarDatosWindow

class App:
    def __init__(self, root):
        self.root = root
        root.title("Interfaz Responsive")
        root.geometry("600x400")

        # Dividir la ventana en dos marcos
        self.left_frame = tk.Frame(root, width=400, height=400, bg="#fff")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(root, width=400, height=400, bg="#f0f0f0")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Agregar imagen circular y texto en el marco izquierdo
        self.img = Image.open("img/imagen.jpeg")
        self.img = self.make_image_circular(self.img, size=(200, 200))
        self.img = ImageTk.PhotoImage(self.img)

        self.img_label = Label(self.left_frame, image=self.img, bg="#fff")
        self.img_label.pack(pady=20)

        self.text_label = tk.Label(self.left_frame, text="MECHI\nEquipo 4\nInteligencia de Negocios\nDr. Luis Mena", bg="#fff", font=("Arial", 16))
        self.text_label.pack(pady=10)

        # Agregar botones en el marco derecho
        self.button_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.button_frame.pack(expand=True, fill=tk.Y, padx=20, pady=20)

        Button(self.button_frame, text="Insertar", font=("Arial", 14), command=self.open_insertar_datos_window).pack(pady=10, fill=tk.X)
        Button(self.button_frame, text="Importar Datos", font=("Arial", 14), command=self.open_import_window).pack(pady=10, fill=tk.X)
        Button(self.button_frame, text="Cerrar", font=("Arial", 14), command=self.close_app).pack(pady=10, fill=tk.X)

    def make_image_circular(self, img, size):
        img = img.resize(size, Image.Resampling.LANCZOS)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        img.putalpha(mask)
        return img

    def open_insertar_datos_window(self):
        InsertarDatosWindow(self.root, self.open_generar_instancias_window)

    def open_import_window(self):
        # Aquí deberías llamar a la ventana de importación cuando esté definida
        pass

    def close_app(self):
        self.root.destroy()

    def open_generar_instancias_window(self, columns, rows):
        from generarInstancias import GenerarInstanciasWindow
        GenerarInstanciasWindow(self.root, columns, rows)

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
