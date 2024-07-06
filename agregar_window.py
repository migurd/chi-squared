import random
import pandas as pd
from PyQt5.QtWidgets import (
  QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QFileDialog,
  QCheckBox, QFormLayout, QHeaderView, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt  # Corrected import statement
from Models.table import Table
from Models.column import Column
from result_window import ResultWindow

class AgregarWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Agregar Datos")
    self.setGeometry(150, 150, 800, 600)

    # Set the application icon
    self.setWindowIcon(QIcon('img/IconLogoMechi.png'))  # Change to your icon path

    self.main_layout = QHBoxLayout(self)  # Change to QHBoxLayout for left-right layout
    self.setStyleSheet("""
      QWidget {
        background-color: #f0f0f0;
      }
      QPushButton {
        background-color: #145c96;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
      }
      QPushButton:hover {
        background-color: #1976D2;
      }
      QLineEdit {
        padding: 2px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 14px;
      }
      QTableWidget {
        background-color: white;
        border: 1px solid #ccc;
      }
      QHeaderView::section {
        background-color: #145c96;
        color: white;
        padding: 5px;
        border: 1px solid #ccc;
      }
      QCheckBox {
        padding: 5px;
        font-size: 14px;
      }
    """)

    # Left panel for buttons and input
    self.left_panel = QVBoxLayout()
    self.left_panel.setSpacing(10)  # Optional: Adjust spacing between elements
    self.main_layout.addLayout(self.left_panel, 1)  # 20% of space

    # Campo para ingresar el nombre de la columna
    self.column_name_input = QLineEdit(self)
    self.column_name_input.setPlaceholderText("Nombre de columna...")
    self.left_panel.addWidget(self.column_name_input)

    # Botones para agregar y eliminar columnas
    self.add_column_button = QPushButton("Agregar Columna", self)
    self.add_column_button.clicked.connect(self.add_column)
    self.add_column_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.add_column_button)

    self.remove_column_button = QPushButton("Eliminar Columna", self)
    self.remove_column_button.clicked.connect(self.remove_column)
    self.remove_column_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.remove_column_button)

    # Botones para agregar y eliminar filas
    self.add_row_button = QPushButton("Agregar Fila", self)
    self.add_row_button.clicked.connect(self.add_row)
    self.add_row_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.add_row_button)

    self.remove_row_button = QPushButton("Eliminar Fila", self)
    self.remove_row_button.clicked.connect(self.remove_row)
    self.remove_row_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.remove_row_button)

    # Botón para limpiar toda la tabla
    self.clear_table_button = QPushButton("Limpiar Tabla", self)
    self.clear_table_button.clicked.connect(self.clear_table)
    self.clear_table_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.clear_table_button)

    # Botón para importar datos
    self.import_data_button = QPushButton("Importar Datos", self)
    self.import_data_button.clicked.connect(self.import_data)
    self.import_data_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.import_data_button)

    # Botón para generar números binarios aleatorios
    self.random_binary_button = QPushButton("Random", self)
    self.random_binary_button.clicked.connect(self.generate_random_binaries)
    self.random_binary_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.random_binary_button)

    # Espaciador para ocupar espacio sobrante
    self.left_panel.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    # Botón para mostrar resultados
    self.show_results_button = QPushButton("Mostrar Resultados", self)
    self.show_results_button.setMinimumHeight(50)
    self.show_results_button.clicked.connect(self.show_results)
    self.show_results_button.setCursor(Qt.PointingHandCursor)  # Updated cursor setting
    self.left_panel.addWidget(self.show_results_button)

    # Right panel for the table and checkboxes
    self.right_panel = QVBoxLayout()
    self.main_layout.addLayout(self.right_panel, 4)  # 80% of space

    # Crear contenedor para las tablas y los checkboxes
    self.table_container = QWidget()
    self.table_layout = QVBoxLayout(self.table_container)
    self.right_panel.addWidget(self.table_container)

    # Crear un layout para checkboxes
    self.checkboxes_layout = QHBoxLayout()
    self.table_layout.addLayout(self.checkboxes_layout)

    # Crear tabla
    self.table = QTableWidget(self)
    self.table_layout.addWidget(self.table)

    self.column_names = []
    self.checkboxes = []

    # Crear objeto Table
    self.data_table = Table()

    # Configure the table to adjust header and wrap text
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.table.horizontalHeader().setStyleSheet("""
      QHeaderView::section { 
        background-color: #145c96; 
        color: white; 
        font-size: 14px;
        font-weight: bold;
      }
    """)
    self.table.setWordWrap(True)

  def add_column(self):
    column_name = self.column_name_input.text().strip()  # Limpiar espacios en blanco

    if isinstance(column_name, str):  # Verificar que column_name es una cadena de texto
      if column_name:
        if column_name in self.column_names:
          QMessageBox.warning(self, "Advertencia", "El nombre de la columna ya existe.")
          return
        if self.table.columnCount() >= 8:
          QMessageBox.warning(self, "Advertencia", "No se pueden agregar más de 8 columnas.")
          return
        current_column_count = self.table.columnCount()
        self.table.insertColumn(current_column_count)
        self.table.setHorizontalHeaderItem(current_column_count, QTableWidgetItem(column_name))
        self.column_names.append(column_name)
        # Añadir un nuevo checkbox
        checkbox = QCheckBox(column_name, self)
        self.checkboxes_layout.addWidget(checkbox)
        self.checkboxes.append(checkbox)
        self.column_name_input.clear()  # Limpiar campo de entrada después de agregar
      else:
        QMessageBox.warning(self, "Advertencia", "El nombre de la columna no puede estar vacío.")
    else:
      QMessageBox.warning(self, "Error", "El valor del campo de entrada no es una cadena de texto.")

  def remove_column(self):
    current_column_count = self.table.columnCount()
    if current_column_count > 0:
      self.table.removeColumn(current_column_count - 1)
      # Remover el último checkbox
      if self.checkboxes:
        checkbox = self.checkboxes.pop()
        self.checkboxes_layout.removeWidget(checkbox)
        checkbox.deleteLater()
      self.column_names.pop()
      # Limpiar tabla si no quedan columnas
      if self.table.columnCount() == 0:
        self.clear_table()
    else:
      QMessageBox.warning(self, "Advertencia", "No hay columnas para eliminar.")

  def add_row(self):
    if self.table.columnCount() > 0:  # Verificar que hay al menos una columna
      row_count = self.table.rowCount()
      self.table.insertRow(row_count)
    else:
      QMessageBox.warning(self, "Advertencia", "Agregue al menos una columna antes de agregar filas.")

  def remove_row(self):
    row_count = self.table.rowCount()
    if row_count > 0:
      self.table.removeRow(row_count - 1)
    else:
      QMessageBox.warning(self, "Advertencia", "No hay filas para eliminar.")

  def clear_table(self):
    self.table.setRowCount(0)
    self.table.setColumnCount(0)
    self.column_names = []
    # Limpiar checkboxes
    for checkbox in self.checkboxes:
      self.checkboxes_layout.removeWidget(checkbox)
      checkbox.deleteLater()
    self.checkboxes = []

  def import_data(self):
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(self, "Abrir archivo de Excel", "", "Archivos Excel (*.xlsx);;Todos los archivos (*)", options=options)

    if file_name:
      try:
        df = pd.read_excel(file_name)

        # Verificar que el archivo tiene datos
        if df.empty:
          QMessageBox.warning(self, "Advertencia", "El archivo está vacío.")
          return

        # Verificar el número de columnas
        if len(df.columns) > 8:
          QMessageBox.warning(self, "Advertencia", "El archivo tiene más de 8 columnas.")
          return

        # Verificar nombres de columnas repetidos
        if any(column in self.column_names for column in df.columns):
          QMessageBox.warning(self, "Advertencia", "El archivo contiene nombres de columnas repetidos.")
          return

        # Limpiar tabla existente antes de cargar nuevos datos
        self.clear_table()

        # Configurar tabla con número de columnas y filas del archivo
        num_columns = len(df.columns)
        num_rows = len(df)

        # Configurar tabla
        self.table.setColumnCount(num_columns)
        self.table.setRowCount(num_rows)
        self.table.setHorizontalHeaderLabels(df.columns)
        self.column_names.extend(df.columns)

        # Crear checkboxes para las columnas
        self.checkboxes = []
        self.checkboxes_layout.setSpacing(10)  # Opcional: ajustar espaciado entre checkboxes

        for i, column in enumerate(df.columns):
          checkbox = QCheckBox(column, self)
          self.checkboxes_layout.addWidget(checkbox)
          self.checkboxes.append(checkbox)

        # Añadir filas con datos y aplicar validación
        for row_index, row in df.iterrows():
          for col_index, value in enumerate(row):
            item = QTableWidgetItem(str(value))
            if str(value) not in ['0', '1']:
              item.setBackground(QColor('#FFCCCC'))  # Indicar error en rojo claro
              item.setToolTip("El valor debe ser 0 o 1.")
            self.table.setItem(row_index, col_index, item)

      except Exception as e:
        QMessageBox.warning(self, "Error", f"Ocurrió un error al leer el archivo: {str(e)}")

  def generate_random_binaries(self):
    for row in range(self.table.rowCount()):
      for col in range(self.table.columnCount()):
        random_value = str(random.randint(0, 1))
        self.table.setItem(row, col, QTableWidgetItem(random_value))

  def show_results(self):
    # Ensure exactly two columns are selected
    selected_checkboxes = [i for i, checkbox in enumerate(self.checkboxes) if checkbox.isChecked()]
    if len(selected_checkboxes) != 2:
      QMessageBox.warning(self, "Advertencia", "Debe seleccionar exactamente dos columnas.")
      return

    # Ensure at least one row is present
    if self.table.rowCount() == 0:
      QMessageBox.warning(self, "Advertencia", "Debe haber al menos una fila en la tabla.")
      return

    # Ensure all values are binary and present
    all_values_valid = True
    for row in range(self.table.rowCount()):
      for col in range(self.table.columnCount()):
        item = self.table.item(row, col)
        if not item or item.text() not in ['0', '1']:
          all_values_valid = False
          break
      if not all_values_valid:
        break

    if not all_values_valid:
      QMessageBox.warning(self, "Advertencia", "Todas las filas deben tener valores válidos (0 o 1).")
      return

    # Update the data_table with the values from the table
    self.data_table.clear_columns()
    for col_index in range(self.table.columnCount()):
      column_data = []
      for row_index in range(self.table.rowCount()):
        item = self.table.item(row_index, col_index)
        column_data.append(int(item.text()))
      column_name = self.table.horizontalHeaderItem(col_index).text()
      column = Column(column_name, column_data)
      self.data_table.add_column(column)

    self.data_table.selected_index_columns = selected_checkboxes
    self.data_table.get_contingency_table()
    self.result_window = ResultWindow(self.data_table)
    self.result_window.show()
