from PyQt5.QtWidgets import (
  QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from models.column import Column
from models.table import Table

class ResultWindow(QWidget):
  """
  Clase que representa la ventana de resultados.
  Muestra los resultados de la tabla de contingencia, confianza y cobertura, factor de dependencia, y chi-cuadrado.
  """

  def __init__(self, table):
    super().__init__()
    self.setWindowTitle("Resultados")
    self.setGeometry(200, 200, 800, 700)

    # Establecer el icono de la aplicación
    self.setWindowIcon(QIcon('img/IconLogoMechi.png'))  # Cambiar a la ruta de tu icono

    self.table = table
    self.init_ui()

  def init_ui(self):
    main_layout = QVBoxLayout()

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    container = QWidget()
    layout = QVBoxLayout(container)

    # Título de la ventana
    title = QLabel("Resultados")
    title.setStyleSheet("font-size: 30px; font-weight: bold; color: #145c96; margin-bottom: 20px;")
    title.setAccessibleName("Resultados")
    title.setAccessibleDescription("Título de la ventana de resultados")
    layout.addWidget(title)

    # Título de la tabla de contingencia
    cont_table_title = QLabel("Tabla de contingencia")
    cont_table_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #145c96; margin-bottom: 10px;")
    cont_table_title.setAccessibleName("Tabla de contingencia")
    cont_table_title.setAccessibleDescription("Título de la tabla de contingencia")
    layout.addWidget(cont_table_title)

    # Tabla de contingencia
    self.create_table(layout, self.table.get_contingency_table(), "contingency")

    # Separador
    layout.addWidget(self.create_separator())

    # Título de confianza y cobertura
    conf_cov_title = QLabel("Confianza y cobertura")
    conf_cov_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #145c96; margin-bottom: 10px;")
    conf_cov_title.setAccessibleName("Confianza y cobertura")
    conf_cov_title.setAccessibleDescription("Título de la sección de confianza y cobertura")
    layout.addWidget(conf_cov_title)

    # Resultados de confianza y cobertura
    coverage_list, confidence_list = self.table.get_coverage_confidence()
    for coverage, confidence in zip(coverage_list, confidence_list):
      coverage_label = QLabel(f"Cobertura: {coverage}")
      confidence_label = QLabel(f"Confianza: {confidence}")
      separator_label = QLabel("." * 100)  # Separador

      coverage_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
      confidence_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 15px;")
      separator_label.setStyleSheet("color: #ccc; margin-bottom: 10px;")

      coverage_label.setAccessibleName("Cobertura")
      coverage_label.setAccessibleDescription(f"Valor de cobertura: {coverage}")
      confidence_label.setAccessibleName("Cobertura")
      confidence_label.setAccessibleDescription(f"Valor de confianza: {confidence}")
      
      layout.addWidget(coverage_label)
      layout.addWidget(confidence_label)
      layout.addWidget(separator_label)

    # Separador
    layout.addWidget(self.create_separator())

    # Título del factor de dependencia
    dep_factor_title = QLabel("Factor de dependencia")
    dep_factor_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #145c96; margin-bottom: 10px;")
    dep_factor_title.setAccessibleName("Factor de dependencia")
    dep_factor_title.setAccessibleDescription("Título de la sección de factor de dependencia")
    layout.addWidget(dep_factor_title)

    # Tabla de factores de dependencia
    self.create_table(layout, self.table.get_dependency_factor(), "dependency")

    # Separador
    layout.addWidget(self.create_separator())

    # Cálculo de chi-cuadrado
    chi_squared_value, chi_squared_steps, result_string = self.table.calculate_chi_squared()
    significance = self.table.determine_significance(chi_squared_value)

    # Título de los resultados de chi-cuadrado
    chi_squared_title = QLabel("Chi-cuadrado")
    chi_squared_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #145c96; margin-bottom: 10px;")
    chi_squared_title.setAccessibleName("Chi-cuadrado")
    chi_squared_title.setAccessibleDescription("Título de la sección de Chi-cuadrado")
    layout.addWidget(chi_squared_title)

    # Mostrar los resultados de chi-cuadrado
    chi_squared_label = QLabel(f"Valor Chi-cuadrado: {chi_squared_value:.4f}\n")
    result_string_label = QLabel(f'{result_string}\n')
    significance_label = QLabel(significance)

    chi_squared_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
    result_string_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
    significance_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 15px;")

    chi_squared_label.setAccessibleName("Valor Chi-cuadrado")
    chi_squared_label.setAccessibleDescription(f"Valor calculado de Chi-cuadrado: {chi_squared_value:.4f}")
    result_string_label.setAccessibleName("Resultado Chi-cuadrado")
    result_string_label.setAccessibleDescription(f"Resultado: {result_string}")
    significance_label.setAccessibleName("Significación")
    significance_label.setAccessibleDescription(f"Significación: {significance}")

    layout.addWidget(result_string_label)
    layout.addWidget(chi_squared_label)
    layout.addWidget(significance_label)

    scroll_area.setWidget(container)
    main_layout.addWidget(scroll_area)
    self.setLayout(main_layout)

  def create_table(self, layout, data, table_type):
    """
    Crea y configura una tabla con los datos proporcionados.

    :param layout: Layout donde se agregará la tabla.
    :param data: Datos a mostrar en la tabla.
    :param table_type: Tipo de tabla (contingencia o dependencia).
    """
    table_size_x = 700
    table_size_y = 250
    if table_type == "contingency":
      name1, name2 = self.table.get_names()
      table = QTableWidget(len(data), len(data[0]))
      table.setHorizontalHeaderLabels([f"{name2}", f"~{name2}", "Σ"])
      table.setVerticalHeaderLabels([f"{name1}", f"~{name1}", "Σ"])
    elif table_type == "dependency":
      name1, name2 = self.table.get_names()
      table = QTableWidget(len(data), len(data[0]))
      table.setHorizontalHeaderLabels([f"{name2}", f"~{name2}"])
      table.setVerticalHeaderLabels([f"{name1}", f"~{name1}"])

    for row in range(len(data)):
      for col in range(len(data[0])):
        item = QTableWidgetItem(str(data[row][col]))
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, col, item)

    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.setFixedSize(table_size_x, table_size_y)
    table.setStyleSheet("""
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
      QTableWidgetItem {
        padding: 2px;
        font-size: 18px;
      }
    """)
    layout.addWidget(table)

  def create_separator(self):
    """
    Crea un separador visual.

    :return: QLabel que actúa como separador.
    """
    separator = QLabel()
    separator.setFixedHeight(20)
    separator.setStyleSheet("background-color: #eee;")
    return separator

if __name__ == "__main__":
  from models.table import Table
  from models.column import Column
  import sys
  from PyQt5.QtWidgets import QApplication

  app = QApplication(sys.argv)
  table = Table()
  # Ejemplo de columnas y datos
  col1 = Column('GO', [0, 1, 1, 0, 1, 0, 0, 1])
  col2 = Column('PS', [1, 0, 1, 1, 1, 0, 1, 0])
  table.add_column(col1)
  table.add_column(col2)
  table.select_index_column(0)
  table.select_index_column(1)
  table.get_contingency_table()

  result_window = ResultWindow(table)
  result_window.show()
  sys.exit(app.exec_())
