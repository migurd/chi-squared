from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
from PyQt5.QtCore import Qt
from Models.column import Column
from Models.table import Table

class ResultWindow(QWidget):
  def __init__(self, table):
    super().__init__()
    self.setWindowTitle("Resultados")
    self.setGeometry(200, 200, 600, 750)
    self.table = table
    self.init_ui()

  def init_ui(self):
    main_layout = QVBoxLayout()

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    container = QWidget()
    layout = QVBoxLayout(container)

    # Title
    title = QLabel("Resultados")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: bold;")
    layout.addWidget(title)

    # Contingency table title
    cont_table_title = QLabel("Tabla de contingencia")
    cont_table_title.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(cont_table_title)

    # Contingency table
    self.create_table(layout, self.table.get_contingency_table(), "contingency")

    # Confidence and coverage title
    conf_cov_title = QLabel("Confianza y cobertura")
    conf_cov_title.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(conf_cov_title)

    # Confidence and coverage results
    coverage_list, confidence_list = self.table.get_coverage_confidence()
    for coverage, confidence in zip(coverage_list, confidence_list):
      layout.addWidget(QLabel(f"{coverage}"))
      layout.addWidget(QLabel(f"{confidence}"))
      layout.addWidget(QLabel("." * 100))  # Separator

    # Dependency factor title
    dep_factor_title = QLabel("Factor de dependencia")
    dep_factor_title.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(dep_factor_title)

    # Dependency factors table
    self.create_table(layout, self.table.get_dependency_factor(), "dependency")

    # Chi-squared calculation
    chi_squared_value, chi_squared_steps, result_string = self.table.calculate_chi_squared()
    significance = self.table.determine_significance(chi_squared_value)

    # Chi-squared results title
    chi_squared_title = QLabel("Chi-cuadrado")
    chi_squared_title.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(chi_squared_title)

    # Display the chi-squared results
    chi_squared_label = QLabel(f"Chi-squared value: {chi_squared_value:.4f}")
    chi_squared_steps_label = QLabel(f"Calculation steps: {chi_squared_steps}")
    result_string_label = QLabel(result_string)
    significance_label = QLabel(significance)

    layout.addWidget(chi_squared_label)
    layout.addWidget(chi_squared_steps_label)
    layout.addWidget(result_string_label)
    layout.addWidget(significance_label)

    scroll_area.setWidget(container)
    main_layout.addWidget(scroll_area)
    self.setLayout(main_layout)

  def create_table(self, layout, data, table_type):
    table_size_x = 500
    table_size_y = 200
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
        table.setItem(row, col, QTableWidgetItem(str(data[row][col])))

    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.setFixedSize(table_size_x, table_size_y)
    layout.addWidget(table)

if __name__ == "__main__":
  from table import Table
  from column import Column
  import sys
  from PyQt5.QtWidgets import QApplication

  app = QApplication(sys.argv)
  table = Table()
  # Example columns and data
  col1 = Column('Pan blanco', [1, 1, 1, 0, 0, 0, 0, 0, 0, 0])
  col2 = Column('Pan integral', [1, 0, 0, 1, 1, 1, 0, 0, 0, 0])
  table.add_column(col1)
  table.add_column(col2)
  table.select_index_column(0)
  table.select_index_column(1)
  table.get_contingency_table()

  result_window = ResultWindow(table)
  result_window.show()
  sys.exit(app.exec_())