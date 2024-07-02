import os
import openpyxl
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class Columna:
    def __init__(self, nombre, valores):
        self.nombre = nombre
        self.valores = []
        for valor in valores:
            if isinstance(valor, str) and valor.strip() in ('0', '1'):
                self.valores.append(int(valor.strip()))
            elif isinstance(valor, int) and valor in (0, 1):
                self.valores.append(valor)
            else:
                raise ValueError(f"Valor no válido en la columna '{nombre}': '{valor}'")

class Tabla:
    def __init__(self, columnas):
        if not (2 <= len(columnas) <= 8):
            raise ValueError("La tabla debe tener entre 2 y 8 columnas")
        self.columnas = columnas

def importar_excel(file_path):
    # Validar que el archivo tenga la extensión .xlsx o .xls
    if not file_path.lower().endswith(('.xlsx', '.xls')):
        raise ValueError("El archivo debe tener la extensión .xlsx o .xls")
    
    # Verificar si el archivo existe
    if not os.path.isfile(file_path):
        raise FileNotFoundError("El archivo no se encontró")
    
    # Cargar el archivo Excel
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    # Leer los datos
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)

    # Validar que haya al menos una fila de datos (excluyendo los encabezados)
    if len(data) <= 1:
        raise ValueError("La cantidad de instancias (datos) debe ser mayor a 0")

    # Extraer nombres de columnas y validar que no estén vacíos
    nombres_columnas = data[0]
    if any(not isinstance(nombre, str) or not nombre.strip() for nombre in nombres_columnas):
        raise ValueError("Todos los nombres de atributos deben estar llenos")

    # Validar que no haya valores None en la primera fila
    if any(valor is None for valor in nombres_columnas):
        raise ValueError("Todos los nombres de atributos deben estar llenos")

    # Extraer y validar los datos de las columnas
    columnas = []
    for col_idx, nombre in enumerate(nombres_columnas):
        valores = [fila[col_idx] for fila in data[1:]]
        # Validar y convertir los valores a enteros
        columna = Columna(nombre, valores)
        columnas.append(columna)

    # Crear la tabla
    tabla = Tabla(columnas)

    return tabla

def seleccionar_archivo():
    # Inicializar Tkinter y ocultar la ventana principal
    root = Tk()
    root.withdraw()
    
    # Abrir el cuadro de diálogo para seleccionar el archivo
    file_path = askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xls")])
    
    return file_path

# Ejemplo de uso
try:
    file_path = seleccionar_archivo()
    if file_path:  # Verificar si se seleccionó un archivo
        tabla = importar_excel(file_path)
        for columna in tabla.columnas:
            print(f"Columna: {columna.nombre}")
            print(f"Valores: {columna.valores}")
    else:
        print("No se seleccionó ningún archivo.")
except ValueError as ve:
    print(f"Error de validación: {ve}")
except FileNotFoundError as fnf:
    print(f"Error de archivo: {fnf}")
except Exception as e:
    print(f"Se produjo un error: {e}")
