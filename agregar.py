import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QFileDialog,
    QCheckBox, QFormLayout
)
from PyQt5.QtCore import Qt


class AgregarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Datos")
        self.setGeometry(150, 150, 800, 600)

        self.main_layout = QVBoxLayout(self)

        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        # Campo para ingresar el nombre de la columna
        self.column_name_input = QLineEdit(self)
        self.column_name_input.setPlaceholderText("Ingrese el nombre de la columna")
        self.column_name_input.setMinimumWidth(200)
        self.top_layout.addWidget(self.column_name_input)

        # Botones para agregar y eliminar columnas
        self.add_column_button = QPushButton("Agregar Columna", self)
        self.add_column_button.clicked.connect(self.add_column)
        self.top_layout.addWidget(self.add_column_button)

        self.remove_column_button = QPushButton("Eliminar Columna", self)
        self.remove_column_button.clicked.connect(self.remove_column)
        self.top_layout.addWidget(self.remove_column_button)

        # Botones para agregar y eliminar filas
        self.add_row_button = QPushButton("Agregar Fila", self)
        self.add_row_button.clicked.connect(self.add_row)
        self.top_layout.addWidget(self.add_row_button)

        self.remove_row_button = QPushButton("Eliminar Fila", self)
        self.remove_row_button.clicked.connect(self.remove_row)
        self.top_layout.addWidget(self.remove_row_button)

        # Botón para limpiar toda la tabla
        self.clear_table_button = QPushButton("Limpiar Tabla", self)
        self.clear_table_button.clicked.connect(self.clear_table)
        self.top_layout.addWidget(self.clear_table_button)

        # Botón para importar datos
        self.import_data_button = QPushButton("Importar Datos", self)
        self.import_data_button.clicked.connect(self.import_data)
        self.top_layout.addWidget(self.import_data_button)

        # Crear tabla
        self.table = QTableWidget(self)
        self.main_layout.addWidget(self.table)

        # Crear un layout para checkboxes
        self.checkboxes_layout = QFormLayout()
        self.checkboxes_container = QWidget()
        self.checkboxes_container.setLayout(self.checkboxes_layout)
        self.main_layout.addWidget(self.checkboxes_container)

        self.column_names = []
        self.checkboxes = []

    def add_column(self):
        column_name = self.column_name_input.text().strip()  # Limpiar espacios en blanco

        # Depuración: Mostrar el valor del campo de entrada y su tipo
        print(f"Valor del campo de entrada: '{column_name}'")
        print(f"Tipo del valor del campo de entrada: {type(column_name)}")

        if isinstance(column_name, str):  # Verificar que column_name es una cadena de texto
            if column_name:
                current_column_count = self.table.columnCount()
                self.table.insertColumn(current_column_count)
                self.table.setHorizontalHeaderItem(current_column_count, QTableWidgetItem(column_name))
                self.column_names.append(column_name)
                # Añadir un nuevo checkbox
                checkbox = QCheckBox(f"Columna {current_column_count + 1}", self)
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

                # Limpiar tabla existente antes de cargar nuevos datos
                self.clear_table()

                # Configurar tabla con número de columnas y filas del archivo
                num_columns = len(df.columns)
                num_rows = len(df)

                # Configurar tabla
                self.table.setColumnCount(num_columns)
                self.table.setRowCount(num_rows)
                self.table.setHorizontalHeaderLabels(df.columns)

                # Crear checkboxes para las columnas
                self.checkboxes = []
                self.checkboxes_layout.setSpacing(10)  # Opcional: ajustar espaciado entre checkboxes

                for i in range(num_columns):
                    checkbox = QCheckBox(f"Columna {i + 1}", self)
                    self.checkboxes_layout.addWidget(checkbox)
                    self.checkboxes.append(checkbox)

                # Añadir filas con datos y aplicar validación
                for row_index, row in df.iterrows():
                    for col_index, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        if str(value) not in ['0', '1']:
                            item.setBackground(Qt.red)  # Indicar error en rojo
                            item.setToolTip("El valor debe ser 0 o 1.")
                        self.table.setItem(row_index, col_index, item)

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Ocurrió un error al leer el archivo: {str(e)}")

    def validate_table(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    value = item.text()
                    if value not in ['0', '1']:
                        item.setBackground(Qt.red)
                        item.setToolTip("El valor debe ser 0 o 1.")
                    else:
                        item.setBackground(Qt.white)
                        item.setToolTip("")
