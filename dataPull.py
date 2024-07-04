import pandas as pd

# Crear un DataFrame con los nuevos datos y nombres
data = {
    'n1': [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    'n2': [1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
}

df = pd.DataFrame(data)

# Generar la tabla de contingencia
contingency_table = pd.crosstab(df['n1'], df['n2'], margins=True)
contingency_table = contingency_table.rename(index={0: '~n1', 1: 'n1'}, columns={0: '~n2', 1: 'n2'})
contingency_table = contingency_table.reindex(['n1', '~n1', 'All'], axis=0).reindex(['n2', '~n2', 'All'], axis=1)
print("Tabla de Contingencia:")
print(contingency_table.to_string(index_names=False, col_space=10))

# Función para calcular cobertura y confianza
def calculate_coverage_confidence(contingency_table, condition):
    total = contingency_table.at['All', 'All']
    coverage_count = total_condition = 0  # Inicializar variables

    if condition == "Si (n1=1) entonces n2=1":
        coverage_count = contingency_table.at['n1', 'n2']
        total_n1 = contingency_table.at['n1', 'All']
        coverage = coverage_count / total
        confidence = coverage_count / total_n1
        total_condition = total_n1
    elif condition == "Si (n1=1) entonces n2=0":
        coverage_count = contingency_table.at['n1', '~n2']
        total_n1 = contingency_table.at['n1', 'All']
        coverage = coverage_count / total
        confidence = coverage_count / total_n1
        total_condition = total_n1
    elif condition == "Si (n1=0) entonces n2=1":
        coverage_count = contingency_table.at['~n1', 'n2']
        total_n0 = contingency_table.at['~n1', 'All']
        coverage = coverage_count / total
        confidence = coverage_count / total_n0
        total_condition = total_n0
    elif condition == "Si (n1=0) entonces n2=0":
        coverage_count = contingency_table.at['~n1', '~n2']
        total_n0 = contingency_table.at['~n1', 'All']
        coverage = coverage_count / total
        confidence = coverage_count / total_n0
        total_condition = total_n0
    elif condition == "Si (n2=1) entonces n1=1":
        coverage_count = contingency_table.at['n1', 'n2']
        total_n2 = contingency_table.at['All', 'n2']
        coverage = coverage_count / total
        confidence = coverage_count / total_n2
        total_condition = total_n2
    elif condition == "Si (n2=1) entonces n1=0":
        coverage_count = contingency_table.at['~n1', 'n2']
        total_n2 = contingency_table.at['All', 'n2']
        coverage = coverage_count / total
        confidence = coverage_count / total_n2
        total_condition = total_n2
    elif condition == "Si (n2=0) entonces n1=1":
        coverage_count = contingency_table.at['n1', '~n2']
        total_n2 = contingency_table.at['All', '~n2']
        coverage = coverage_count / total
        confidence = coverage_count / total_n2
        total_condition = total_n2
    elif condition == "Si (n2=0) entonces n1=0":
        coverage_count = contingency_table.at['~n1', '~n2']
        total_n2 = contingency_table.at['All', '~n2']
        coverage = coverage_count / total
        confidence = coverage_count / total_n2
        total_condition = total_n2
    else:
        coverage = confidence = None
    
    return coverage, confidence, coverage_count, total_condition

# Condiciones para calcular cobertura y confianza
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

# Calcular y mostrar la cobertura y confianza para cada condición
for condition in conditions:
    coverage, confidence, coverage_count, total_condition = calculate_coverage_confidence(contingency_table, condition)
    if coverage is not None and confidence is not None:
        print(f"{condition}: Cobertura = {coverage*100:.2f}% ({coverage_count}/{contingency_table.at['All', 'All']}), Confianza = {confidence*100:.2f}% ({coverage_count}/{total_condition})")
    else:
        print(f"{condition}: No se pudo calcular cobertura y confianza")

# Función para calcular el factor de dependencia
def calculate_dependency_factor(contingency_table):
    total = contingency_table.at['All', 'All']
    factors = pd.DataFrame(index=['n1', '~n1'], columns=['n2', '~n2'])

    for i in ['n1', '~n1']:
        for j in ['n2', '~n2']:
            P_i_and_j = contingency_table.at[i, j] / total
            P_i = contingency_table.at[i, 'All'] / total
            P_j = contingency_table.at['All', j] / total
            if P_i * P_j != 0:
                FD = P_i_and_j / (P_i * P_j)
            else:
                FD = 0
            factors.at[i, j] = round(FD, 3)  # Redondear a 3 decimales

    return factors

# Calcular el factor de dependencia
dependency_factors = calculate_dependency_factor(contingency_table)
print("\nFactor de Dependencia:")
print(dependency_factors.to_string(index_names=False, col_space=10))