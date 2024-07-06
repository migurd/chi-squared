import math
import pandas as pd
from .column import Column
from typing import List, Tuple

class Table:
  def __init__(self):
    self.columns = []
    self.selected_index_columns = []
    self.contingency_table = None

  def select_index_column(self, index: int):
    if index not in self.selected_index_columns:
      self.selected_index_columns.append(index)

  def add_column(self, new_column: Column):
    self.columns.append(new_column)

  def clear_columns(self):
    self.columns = []

  def are_all_columns_binary(self) -> bool:
    return all(all(value in (0, 1) for value in column.values) for column in self.columns)

  def get_names(self) -> Tuple[str, str]:
    name1 = self.columns[self.selected_index_columns[0]].name
    name2 = self.columns[self.selected_index_columns[1]].name
    return name1, name2

  # Create a DataFrame with the new data and names
  def get_contingency_table(self) -> List[List[int]]:
    name1, name2 = self.get_names()
    
    # Prepare the data for DataFrame
    data = {
      name1: self.columns[self.selected_index_columns[0]].values,
      name2: self.columns[self.selected_index_columns[1]].values
    }

    df = pd.DataFrame(data)

    # Generate the contingency table
    self.contingency_table = pd.crosstab(df[name1], df[name2], margins=True)
    self.contingency_table = self.contingency_table.rename(index={0: f'~{name1}', 1: name1}, columns={0: f'~{name2}', 1: name2})
    self.contingency_table = self.contingency_table.reindex([name1, f'~{name1}', 'All'], axis=0).reindex([name2, f'~{name2}', 'All'], axis=1)

    return self.contingency_table.values.tolist()

  # Función para calcular cobertura y confianza
  def calculate_coverage_confidence(self, condition):
    name1, name2 = self.get_names()
    total = self.contingency_table.at['All', 'All']
    coverage_count = total_condition = 0  # Inicializar variables

    if condition == f"Si ({name1}=1) entonces {name2}=1":
      coverage_count = self.contingency_table.at[name1, name2]
      total_n1 = self.contingency_table.at[name1, 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n1
      total_condition = total_n1
    elif condition == f"Si ({name1}=1) entonces {name2}=0":
      coverage_count = self.contingency_table.at[name1, f'~{name2}']
      total_n1 = self.contingency_table.at[name1, 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n1
      total_condition = total_n1
    elif condition == f"Si ({name1}=0) entonces {name2}=1":
      coverage_count = self.contingency_table.at[f'~{name1}', name2]
      total_n0 = self.contingency_table.at[f'~{name1}', 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n0
      total_condition = total_n0
    elif condition == f"Si ({name1}=0) entonces {name2}=0":
      coverage_count = self.contingency_table.at[f'~{name1}', f'~{name2}']
      total_n0 = self.contingency_table.at[f'~{name1}', 'All']
      coverage = coverage_count / total
      confidence = coverage_count / total_n0
      total_condition = total_n0
    elif condition == f"Si ({name2}=1) entonces {name1}=1":
      coverage_count = self.contingency_table.at[name1, name2]
      total_n2 = self.contingency_table.at['All', name2]
      coverage = coverage_count / total
      confidence = coverage_count / total_n2
      total_condition = total_n2
    elif condition == f"Si ({name2}=1) entonces {name1}=0":
      coverage_count = self.contingency_table.at[f'~{name1}', name2]
      total_n2 = self.contingency_table.at['All', name2]
      coverage = coverage_count / total
      confidence = coverage_count / total_n2
      total_condition = total_n2
    elif condition == f"Si ({name2}=0) entonces {name1}=1":
      coverage_count = self.contingency_table.at[name1, f'~{name2}']
      total_n2 = self.contingency_table.at['All', f'~{name2}']
      coverage = coverage_count / total
      confidence = coverage_count / total_n2
      total_condition = total_n2
    elif condition == f"Si ({name2}=0) entonces {name1}=0":
      coverage_count = self.contingency_table.at[f'~{name1}', f'~{name2}']
      total_n2 = self.contingency_table.at['All', f'~{name2}']
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
    name1, name2 = self.get_names()
    conditions = [
      f"Si ({name1}=1) entonces {name2}=1",
      f"Si ({name1}=1) entonces {name2}=0",
      f"Si ({name1}=0) entonces {name2}=1",
      f"Si ({name1}=0) entonces {name2}=0",
      f"Si ({name2}=1) entonces {name1}=1",
      f"Si ({name2}=1) entonces {name1}=0",
      f"Si ({name2}=0) entonces {name1}=1",
      f"Si ({name2}=0) entonces {name1}=0"
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
    name1, name2 = self.get_names()
    total = self.contingency_table.at['All', 'All']
    factors = pd.DataFrame(index=[name1, f'~{name1}'], columns=[name2, f'~{name2}'])

    for i in [name1, f'~{name1}']:
      for j in [name2, f'~{name2}']:
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
    return dependency_factors.values.tolist()

  def __repr__(self):
    return f"Table(columns={self.columns})"

  def calculate_chi_squared(self) -> Tuple[float, str]:
    # Ensure the contingency table is available
    if self.contingency_table is None:
      self.get_contingency_table()
    
    name1, name2 = self.get_names()
    
    # Observed values
    o_11 = self.contingency_table.at[name1, name2]
    o_12 = self.contingency_table.at[name1, f'~{name2}']
    o_21 = self.contingency_table.at[f'~{name1}', name2]
    o_22 = self.contingency_table.at[f'~{name1}', f'~{name2}']
    
    # Marginal totals
    n1_total = self.contingency_table.at[name1, 'All']
    n0_total = self.contingency_table.at[f'~{name1}', 'All']
    total_n2 = self.contingency_table.at['All', name2]
    total_n0 = self.contingency_table.at['All', f'~{name2}']
    grand_total = self.contingency_table.at['All', 'All']

    # Expected values
    e_11 = (n1_total * total_n2) / grand_total
    e_12 = (n1_total * total_n0) / grand_total
    e_21 = (n0_total * total_n2) / grand_total
    e_22 = (n0_total * total_n0) / grand_total

    # Chi-squared calculation components
    n1 = (o_11 - e_11)**2 / e_11
    n2 = (o_12 - e_12)**2 / e_12
    n3 = (o_21 - e_21)**2 / e_21
    n4 = (o_22 - e_22)**2 / e_22

    # Sum of components to get chi-squared value
    chi_squared = n1 + n2 + n3 + n4

    # Detailed calculation steps
    steps = (
      f"({o_11} - {e_11:.2f})^2 / {e_11:.2f} = {n1:.4f}, "
      f"({o_12} - {e_12:.2f})^2 / {e_12:.2f} = {n2:.4f}, "
      f"({o_21} - {e_21:.2f})^2 / {e_21:.2f} = {n3:.4f}, "
      f"({o_22} - {e_22:.2f})^2 / {e_22:.2f} = {n4:.4f}"
    )
    result_string = f"X^2 = {n1:.4f} + {n2:.4f} + {n3:.4f} + {n4:.4f} = {chi_squared:.4f}"

    return chi_squared, steps, result_string

  def determine_significance(self, chi_squared: float) -> str:
    # Degrees of freedom for a 2x2 table is (rows-1) * (cols-1) = 1
    df = 1
    
    # Critical values for chi-squared distribution with df=1
    critical_values = {
      '95%': 3.84,
      '99%': 6.63,
      '99.99%': 15.1367
    }
    
    # Initialize significance and messages
    significance = "No se rechaza hipótesis de independencia"
    messages = []

    if chi_squared > critical_values['95%']:
      significance = "Dependientes por confianza de 95%"
      messages.append(f"{chi_squared:.4f} > {critical_values['95%']}, entonces SÍ se rechaza hipótesis de independencia con confianza de 95%")
    else:
      messages.append(f"{chi_squared:.4f} < {critical_values['95%']}, entonces NO se rechaza hipótesis de independencia con confianza de 95%")
    if chi_squared > critical_values['99%']:
      significance = "Dependientes por confianza de 99%"
      messages.append(f"{chi_squared:.4f} > {critical_values['99%']}, entonces SÍ se rechaza hipótesis de independencia con confianza de 99%")
    else:
      messages.append(f"{chi_squared:.4f} < {critical_values['99%']}, entonces NO se rechaza hipótesis de independencia con confianza de 99%")
    if chi_squared > critical_values['99.99%']:
      significance = "Dependientes por confianza de 99.99%"
      messages.append(f"{chi_squared:.4f} > {critical_values['99.99%']}, entonces SÍ se rechaza hipótesis de independencia con confianza de 99.99%")
    else:
      messages.append(f"{chi_squared:.4f} < {critical_values['99.99%']}, entonces NO se rechaza hipótesis de independencia con confianza de 99.99%")
    
    return significance + "\n" + "\n".join(messages)