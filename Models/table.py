import math
import pandas as pd
from typing import List, Tuple

class Column:
  """
  Clase que representa una columna en una tabla, con un nombre y una lista de valores binarios (0 o 1).
  """

  def __init__(self, name: str, values: List[int]):
    self.name = name
    self.values = values

class Table:
  """
  Clase que representa una tabla que contiene varias columnas. Proporciona métodos para seleccionar columnas, 
  calcular tablas de contingencia, cobertura, confianza, factor de dependencia, chi-cuadrado y determinar significancia.
  """

  def __init__(self):
    self.columns = []
    self.selected_index_columns = []
    self.contingency_table = None

  def select_index_column(self, index: int):
    """
    Selecciona una columna por su índice para su uso en la generación de tablas de contingencia.

    :param index: Índice de la columna a seleccionar.
    """
    self.selected_index_columns.append(index)

  def add_column(self, new_column: Column):
    """
    Agrega una nueva columna a la tabla.

    :param new_column: Instancia de la clase Column que se va a agregar.
    """
    self.columns.append(new_column)

  def clear_columns(self):
    """
    Elimina todas las columnas de la tabla.
    """
    self.columns = []

  def are_all_columns_binary(self) -> bool:
    """
    Verifica si todos los valores en todas las columnas son binarios (0 o 1).

    :return: True si todos los valores son binarios, False en caso contrario.
    """
    return all(all(value in (0, 1) for value in column.values) for column in self.columns)

  def get_names(self) -> Tuple[str, str]:
    """
    Obtiene los nombres de las columnas seleccionadas.

    :return: Una tupla con los nombres de las dos columnas seleccionadas.
    """
    name1 = self.columns[self.selected_index_columns[0]].name
    name2 = self.columns[self.selected_index_columns[1]].name
    return name1, name2

  def get_contingency_table(self) -> List[List[int]]:
    """
    Genera una tabla de contingencia a partir de las columnas seleccionadas y la retorna como una lista de listas.

    :return: Tabla de contingencia como lista de listas.
    """
    name1, name2 = self.get_names()
    
    # Preparar los datos para DataFrame
    data = {
      name1: self.columns[self.selected_index_columns[0]].values,
      name2: self.columns[self.selected_index_columns[1]].values
    }

    df = pd.DataFrame(data)

    # Generar la tabla de contingencia
    self.contingency_table = pd.crosstab(df[name1], df[name2], margins=True)
    self.contingency_table = self.contingency_table.rename(index={0: f'~{name1}', 1: name1}, columns={0: f'~{name2}', 1: name2})
    self.contingency_table = self.contingency_table.reindex([name1, f'~{name1}', 'All'], axis=0).reindex([name2, f'~{name2}', 'All'], axis=1)

    # Rellenar valores NaN con ceros
    self.contingency_table = self.contingency_table.fillna(0)

    return self.contingency_table.values.tolist()

  def calculate_coverage_confidence(self, condition):
    """
    Calcula la cobertura y confianza para una condición dada.

    :param condition: Condición a evaluar.
    :return: Una tupla con cobertura, confianza, número de ocurrencias de la condición y el total de ocurrencias de la condición.
    """
    name1, name2 = self.get_names()
    total = self.contingency_table.at['All', 'All']
    coverage_count = total_condition = 0  # Inicializar variables

    if condition == f"Si ({name1}=1) entonces {name2}=1":
      coverage_count = self.contingency_table.at[name1, name2]
      total_n = self.contingency_table.at[name1, 'All']
    elif condition == f"Si ({name1}=1) entonces {name2}=0":
      coverage_count = self.contingency_table.at[name1, f'~{name2}']
      total_n = self.contingency_table.at[name1, 'All']
    elif condition == f"Si ({name1}=0) entonces {name2}=1":
      coverage_count = self.contingency_table.at[f'~{name1}', name2]
      total_n = self.contingency_table.at[f'~{name1}', 'All']
    elif condition == f"Si ({name1}=0) entonces {name2}=0":
      coverage_count = self.contingency_table.at[f'~{name1}', f'~{name2}']
      total_n = self.contingency_table.at[f'~{name1}', 'All']
    elif condition == f"Si ({name2}=1) entonces {name1}=1":
      coverage_count = self.contingency_table.at[name1, name2]
      total_n = self.contingency_table.at['All', name2]
    elif condition == f"Si ({name2}=1) entonces {name1}=0":
      coverage_count = self.contingency_table.at[f'~{name1}', name2]
      total_n = self.contingency_table.at['All', name2]
    elif condition == f"Si ({name2}=0) entonces {name1}=1":
      coverage_count = self.contingency_table.at[name1, f'~{name2}']
      total_n = self.contingency_table.at['All', f'~{name2}']
    elif condition == f"Si ({name2}=0) entonces {name1}=0":
      coverage_count = self.contingency_table.at[f'~{name1}', f'~{name2}']
      total_n = self.contingency_table.at['All', f'~{name2}']
    else:
      coverage = confidence = None
      return coverage, confidence, coverage_count, total_condition

    # Calcular cobertura
    coverage = coverage_count / total if total != 0 else 0
    
    # Calcular confianza basada en la condición
    confidence = coverage_count / total_n if total_n != 0 else 0
    total_condition = total_n

    return coverage, confidence, coverage_count, total_condition

  def get_coverage_confidence(self) -> Tuple[List[str], List[str]]:
    """
    Calcula la cobertura y confianza para varias condiciones predefinidas y las retorna como listas de cadenas.

    :return: Dos listas, una con resultados de cobertura y otra con resultados de confianza.
    """
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

  def calculate_dependency_factor(self):
    """
    Calcula el factor de dependencia para cada combinación posible de valores en las columnas seleccionadas.

    :return: DataFrame con los factores de dependencia.
    """
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
    """
    Retorna los factores de dependencia como una lista de listas.

    :return: Lista de listas con los factores de dependencia.
    """
    dependency_factors = self.calculate_dependency_factor()
    return dependency_factors.values.tolist()

  def __repr__(self):
    return f"Table(columns={self.columns})"

  def calculate_chi_squared(self) -> Tuple[float, str]:
    """
    Calcula el valor de chi-cuadrado para las columnas seleccionadas.

    :return: Tupla con el valor de chi-cuadrado, los pasos del cálculo y el resultado final en formato de cadena.
    """
    if self.contingency_table is None:
      self.get_contingency_table()
    
    name1, name2 = self.get_names()
    
    # Valores observados
    o_11 = self.contingency_table.at[name1, name2]
    o_12 = self.contingency_table.at[name1, f'~{name2}']
    o_21 = self.contingency_table.at[f'~{name1}', name2]
    o_22 = self.contingency_table.at[f'~{name1}', f'~{name2}']
    
    # Totales marginales
    n1_total = self.contingency_table.at[name1, 'All']
    n0_total = self.contingency_table.at[f'~{name1}', 'All']
    total_n2 = self.contingency_table.at['All', name2]
    total_n0 = self.contingency_table.at['All', f'~{name2}']
    grand_total = self.contingency_table.at['All', 'All']

    # Valores esperados
    e_11 = (n1_total * total_n2) / grand_total
    e_12 = (n1_total * total_n0) / grand_total
    e_21 = (n0_total * total_n2) / grand_total
    e_22 = (n0_total * total_n0) / grand_total

    # Componentes del cálculo de chi-cuadrado
    n1 = (o_11 - e_11)**2 / e_11 if e_11 != 0 else 0
    n2 = (o_12 - e_12)**2 / e_12 if e_12 != 0 else 0
    n3 = (o_21 - e_21)**2 / e_21 if e_21 != 0 else 0
    n4 = (o_22 - e_22)**2 / e_22 if e_22 != 0 else 0

    # Suma de componentes para obtener el valor de chi-cuadrado
    chi_squared = n1 + n2 + n3 + n4

    # Pasos detallados del cálculo
    steps = (
      f"({o_11} - {e_11:.2f})^2 / {e_11:.2f} = {n1:.4f}, "
      f"({o_12} - {e_12:.2f})^2 / {e_12:.2f} = {n2:.4f}, "
      f"({o_21} - {e_21:.2f})^2 / {e_21:.2f} = {n3:.4f}, "
      f"({o_22} - {e_22:.2f})^2 / {e_22:.2f} = {n4:.4f}"
    )
    result_string = f"X^2 = {n1:.4f} + {n2:.4f} + {n3:.4f} + {n4:.4f} = {chi_squared:.4f}"

    return chi_squared, steps, result_string

  def determine_significance(self, chi_squared: float) -> str:
    """
    Determina la significancia del valor de chi-cuadrado calculado.

    :param chi_squared: Valor de chi-cuadrado calculado.
    :return: Una cadena que indica el nivel de significancia y las comparaciones con valores críticos.
    """
    # Grados de libertad para una tabla 2x2 es (filas-1) * (columnas-1) = 1
    df = 1
    
    # Valores críticos para la distribución chi-cuadrado con df=1
    critical_values = {
      '95%': 3.84,
      '99%': 6.63,
      '99.99%': 15.1367
    }
    
    # Inicializar significancia y mensajes
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

if __name__ == "__main__":
  # Creando instancias de Column
  col1 = Column('Pan blanco', [1, 1, 1, 0, 0, 0, 0, 0, 0, 0])
  col2 = Column('Pan integral', [1, 0, 0, 1, 1, 1, 0, 0, 0, 0])

  # Creando una instancia de Table
  table = Table()

  # Agregando columnas a la tabla
  table.add_column(col1)
  table.add_column(col2)

  # Seleccionando columnas
  table.select_index_column(0)
  table.select_index_column(1)

  # Verificando si todos los valores de las columnas son binarios
  print(f"All columns are binary: {table.are_all_columns_binary()}")
  
  # Obtener tabla de contingencia
  contingency_table = table.get_contingency_table()
  print(f'Tabla de contingencia: \n{contingency_table}')

  # Obtener cobertura y confianza
  coverage_results, confidence_results = table.get_coverage_confidence()
  for coverage, confidence in zip(coverage_results, confidence_results):
    print(coverage)
    print(confidence)

  # Obtener factor de dependencia
  dependency_fator = table.get_dependency_factor()
  print(f'Tabla de dependencia: \n{dependency_fator}')

  # Imprimir las columnas de la tabla
  for col in table.columns:
    print(f"Column Name: {col.name}, Column Values: {col.values}")

  # Obtener valor de chi-cuadrado, pasos de cálculo y cadena de resultados
  chi_squared_value, chi_squared_steps, result_string = table.calculate_chi_squared()
  print(f"Chi-squared value: {chi_squared_value}")
  print(f"Calculation steps: {chi_squared_steps}")
  print(result_string)

  # Determinar significancia
  significance = table.determine_significance(chi_squared_value)
  print(f"Significance: {significance}")
