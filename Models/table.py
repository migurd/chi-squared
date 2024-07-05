from .column import Column
import pandas as pd
from typing import List, Tuple

class Table:
  columns = []  # Obj Column
  selected_index_columns: List[int] = []  # int indexes
  contingency_table = None

  def __init__(self):
    pass

  def select_index_column(self, index: int):
    self.selected_index_columns.append(index)

  def add_column(self, new_column : Column):
    self.columns.append(new_column)

  def clear_columns(self):
    self.columns = []

  def are_all_columns_binary(self) -> bool:
    return all(all(value in (0, 1) for value in column.values) for column in self.columns)

  # Create a DataFrame with the new data and names
  def get_contingency_table(self) -> List[List[int]]:
    # Prepare the data for DataFrame
    data = {
      self.columns[self.selected_index_columns[0]].name: self.columns[self.selected_index_columns[0]].values,
      self.columns[self.selected_index_columns[1]].name: self.columns[self.selected_index_columns[1]].values
    }

    df = pd.DataFrame(data)

    # Generate the contingency table
    self.contingency_table = pd.crosstab(df[self.columns[self.selected_index_columns[0]].name], df[self.columns[self.selected_index_columns[1]].name], margins=True)
    self.contingency_table = self.contingency_table.rename(index={0: '~n1', 1: 'n1'}, columns={0: '~n2', 1: 'n2'})
    self.contingency_table = self.contingency_table.reindex(['n1', '~n1', 'All'], axis=0).reindex(['n2', '~n2', 'All'], axis=1)
    
    # print("Tabla de Contingencia:")
    # print(self.contingency_table.to_string(index_names=False, col_space=10))

    return self.contingency_table.values.tolist()

  # Función para calcular cobertura y confianza
  def calculate_coverage_confidence(self, condition):
    total = self.contingency_table.at['All', 'All']
    coverage_count = total_condition = 0  # Inicializar variables

    if condition == "Si (n1=1) entonces n2=1":
      coverage_count = self.contingency_table.at['n1', 'n2']
      total_n1 = self.contingency_table.at['n1', 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n1
      total_condition = total_n1
    elif condition == "Si (n1=1) entonces n2=0":
      coverage_count = self.contingency_table.at['n1', '~n2']
      total_n1 = self.contingency_table.at['n1', 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n1
      total_condition = total_n1
    elif condition == "Si (n1=0) entonces n2=1":
      coverage_count = self.contingency_table.at['~n1', 'n2']
      total_n0 = self.contingency_table.at['~n1', 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n0
      total_condition = total_n0
    elif condition == "Si (n1=0) entonces n2=0":
      coverage_count = self.contingency_table.at['~n1', '~n2']
      total_n0 = self.contingency_table.at['~n1', 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n0
      total_condition = total_n0
    elif condition == "Si (n2=1) entonces n1=1":
      coverage_count = self.contingency_table.at['n1', 'n2']
      total_n2 = self.contingency_table.at['All', 'n2']
      coverage = coverage_count / total
      confidence = coverage_count / total_n2
      total_condition = total_n2
    elif condition == "Si (n2=1) entonces n1=0":
      coverage_count = self.contingency_table.at['~n1', 'n2']
      total_n2 = self.contingency_table.at['All', 'n2']
      coverage = coverage_count / total
      confidence = coverage_count / total_n2
      total_condition = total_n2
    elif condition == "Si (n2=0) entonces n1=1":
      coverage_count = self.contingency_table.at['n1', '~n2']
      total_n2 = self.contingency_table.at['All', '~n2']
      coverage = coverage_count / total
      confidence = coverage_count / total_n2
      total_condition = total_n2
    elif condition == "Si (n2=0) entonces n1=0":
      coverage_count = self.contingency_table.at['~n1', '~n2']
      total_n2 = self.contingency_table.at['All', '~n2']
      coverage = coverage_count / total
      confidence = coverage_count / total_n2
      total_condition = total_n2
    else:
      coverage = confidence = None
    
    return coverage, confidence, coverage_count, total_condition

  # Condiciones para calcular cobertura y confianza
  def get_coverage_confidence(self) -> Tuple[List[str], List[str]]:
    coverage_list = []
    confidence_list = []
    conditions = [
      "Si (n1=1) entonces n2=1",
      "Si (n1=1) entonces n2=0",
      "Si (n1=0) entonces n2=1",
      "Si (n1=0) entonces n2=0",
      "Si (n2=1) entonces n1=1",
      "Si (n2=1) entonces n1=0",
      "Si (n2=0) entonces n1=1",
      "Si (n2=0) entonces n1=0"
    ]

    # Calcular y almacenar la cobertura y confianza para cada condición
    for condition in conditions:
      coverage, confidence, coverage_count, total_condition = self.calculate_coverage_confidence(condition)
      if coverage is not None and confidence is not None:
        coverage_result = (f"{condition}: Cobertura = {coverage*100:.2f}% "
                           f"({coverage_count}/{self.contingency_table.at['All', 'All']})")
        confidence_result = (f"{condition}: Confianza = {confidence*100:.2f}% "
                             f"({coverage_count}/{total_condition})")
      else:
        coverage_result = f"{condition}: No se pudo calcular cobertura"
        confidence_result = f"{condition}: No se pudo calcular confianza"
      
      coverage_list.append(coverage_result)
      confidence_list.append(confidence_result)

    return coverage_list, confidence_list

  # Función para calcular el factor de dependencia
  def calculate_dependency_factor(self):
    total = self.contingency_table.at['All', 'All']
    factors = pd.DataFrame(index=['n1', '~n1'], columns=['n2', '~n2'])

    for i in ['n1', '~n1']:
      for j in ['n2', '~n2']:
        P_i_and_j = self.contingency_table.at[i, j] / total
        P_i = self.contingency_table.at[i, 'All'] / total
        P_j = self.contingency_table.at['All', j] / total
        if P_i * P_j != 0:
          FD = P_i_and_j / (P_i * P_j)
        else:
          FD = 0
        factors.at[i, j] = round(FD, 3)  # Redondear a 3 decimales
    return factors
  
  def get_dependency_factor(self) -> List[List[int]]:
    dependency_factors = self.calculate_dependency_factor()
    # print("\nFactor de Dependencia:")
    # print(dependency_factors.to_string(index_names=False, col_space=10))
    return dependency_factors.values.tolist()
  
  def __repr__(self):
    return f"Table(columns={self.columns})"

if __name__ == "__main__":
  # Creating Column instances
  col1 = Column('Pan blanco',[1, 1, 1, 0, 0, 0, 0, 0, 0, 0])
  col2 = Column('Pan integral', [1, 0, 0, 1, 1, 1, 0, 0, 0, 0])

  # Creating a Table instance
  table = Table()

  # Adding columns to the table
  table.add_column(col1)
  table.add_column(col2)

  # Select columns
  table.select_index_column(0)
  table.select_index_column(1)

  # Checking if all column values are binary
  print(f"All columns are binary: {table.are_all_columns_binary()}")

  # Check contingency table
  contingency_table = table.get_contingency_table()
  print(f'Tabla de contingencia: \n{contingency_table}')

  # Get coverage and confidence
  coverage_results, confidence_results = table.get_coverage_confidence()
  for coverage, confidence in zip(coverage_results, confidence_results):
    print(coverage)
    print(confidence)

  # Check dependency factor
  dependency_fator = table.get_dependency_factor()
  print(f'Tabla de depenendencia: \n{dependency_fator}')

  # Printing the table's columns
  for col in table.columns:
    print(f"Column Name: {col.name}, Column Values: {col.values}")