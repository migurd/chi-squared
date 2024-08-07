import math
import pandas as pd
from typing import List, Tuple
from .column import Column

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
        if index not in self.selected_index_columns:
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
        if len(self.selected_index_columns) < 2:
            raise ValueError("Se deben seleccionar exactamente dos columnas.")
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
        self.contingency_table = self.contingency_table.rename(
            index={0: f'~{name1}', 1: name1},
            columns={0: f'~{name2}', 1: name2}
        )
        self.contingency_table = self.contingency_table.reindex(
            [name1, f'~{name1}', 'All'], axis=0
        ).reindex([name2, f'~{name2}', 'All'], axis=1)

        # Rellenar valores NaN con ceros
        self.contingency_table = self.contingency_table.fillna(0)

        return self.contingency_table.values.tolist()

    def calculate_coverage_confidence(self, condition: str) -> Tuple[float, float, int, int]:
        """
        Calcula la cobertura y confianza para una condición dada.

        :param condition: Condición a evaluar.
        :return: Una tupla con cobertura, confianza, número de ocurrencias de la condición y el total de ocurrencias de la condición.
        """
        name1, name2 = self.get_names()
        total = self.contingency_table.at['All', 'All']
        coverage_count = total_n = 0  # Inicializar variables

        condition_map = {
            f"Si ({name1}=1) entonces {name2}=1": (name1, name2),
            f"Si ({name1}=1) entonces {name2}=0": (name1, f'~{name2}'),
            f"Si ({name1}=0) entonces {name2}=1": (f'~{name1}', name2),
            f"Si ({name1}=0) entonces {name2}=0": (f'~{name1}', f'~{name2}'),
            f"Si ({name2}=1) entonces {name1}=1": (name1, name2),
            f"Si ({name2}=1) entonces {name1}=0": (f'~{name1}', name2),
            f"Si ({name2}=0) entonces {name1}=1": (name1, f'~{name2}'),
            f"Si ({name2}=0) entonces {name1}=0": (f'~{name1}', f'~{name2}')
        }

        if condition in condition_map:
            row, col = condition_map[condition]
            coverage_count = self.contingency_table.at[row, col]
            total_n = self.contingency_table.at[row, 'All']
        else:
            return None, None, coverage_count, total_n

        # Calcular cobertura
        coverage = coverage_count / total if total != 0 else 0
        
        # Calcular confianza basada en la condición
        confidence = coverage_count / total_n if total_n != 0 else 0
        return coverage, confidence, coverage_count, total_n

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

    def calculate_dependency_factor(self) -> pd.DataFrame:
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
                FD = P_i_and_j / (P_i * P_j) if P_i * P_j != 0 else 0
                factors.at[i, j] = round(FD, 3)  # Redondear a 3 decimales
        return factors

    def get_dependency_factor(self) -> List[List[float]]:
        """
        Retorna los factores de dependencia como una lista de listas.

        :return: Lista de listas con los factores de dependencia.
        """
        dependency_factors = self.calculate_dependency_factor()
        return dependency_factors.values.tolist()

    def __repr__(self) -> str:
        return f"Table(columns={self.columns})"

    def calculate_chi_squared(self) -> Tuple[float, str, str]:
        """
        Calcula el valor de chi-cuadrado para las columnas seleccionadas.

        :return: Tupla con el valor de chi-cuadrado, los pasos del cálculo y el resultado final en formato de cadena.
        """
        if self.contingency_table is None:
            self.get_contingency_table()  # Asegurarse de que la tabla de contingencia esté calculada

        total = self.contingency_table.at['All', 'All']
        chi_squared = 0
        steps = []
        for i in [self.columns[self.selected_index_columns[0]].name, f'~{self.columns[self.selected_index_columns[0]].name}']:
            for j in [self.columns[self.selected_index_columns[1]].name, f'~{self.columns[self.selected_index_columns[1]].name}']:
                observed = self.contingency_table.at[i, j]
                expected = (self.contingency_table.at[i, 'All'] * self.contingency_table.at['All', j]) / total
                step = f"({i}, {j}) Observado: {observed}, Esperado: {expected}, (O-E)^2/E: {((observed - expected) ** 2) / expected if expected != 0 else 0}"
                steps.append(step)
                chi_squared += (observed - expected) ** 2 / expected if expected != 0 else 0

        return chi_squared, "\n".join(steps), f"Valor de Chi-cuadrado = {chi_squared:.2f}"

    def is_significant(self, chi_squared: float, df: int) -> str:
        """
        Determina si el valor de chi-cuadrado es significativo basándose en el nivel de significancia del 5%.

        :param chi_squared: Valor de chi-cuadrado calculado.
        :param df: Grados de libertad.
        :return: Cadena que indica si el valor es significativo.
        """
        chi_squared_critical = 5.99  # Valor crítico de chi-cuadrado para 1 grado de libertad y nivel de significancia del 5%
        significance = "Significativo" if chi_squared > chi_squared_critical else "No significativo"
        return f"Valor de Chi-cuadrado: {chi_squared:.2f}, Nivel de Significancia: {significance}"

