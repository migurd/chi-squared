# MECHI - Chi2 - Análisis Estadístico con Prueba Chi-Cuadrado

## Descripción
Este programa es una aplicación en Python que realiza análisis estadísticos mediante la Prueba Chi-Cuadrado. Permite la carga manual y automatizada de datos, construcción de tablas de contingencia, cálculo de valores de confianza y cobertura para reglas de 2 ítems, y determinación de la significancia del valor de dependencia.

![Mechi Logo](https://imgur.com/zhrC4Ar.png)

## Requisitos Previos
Para utilizar este programa, es necesario contar con Python 3.6 o superior. Asegúrese de tener Python instalado en su sistema. Puede verificar la versión instalada usando el comando `python --version` o `python3 --version`.

También se recomienda utilizar un entorno virtual para manejar las dependencias del proyecto. Esto asegura que las dependencias del proyecto no interfieran con otras instalaciones de Python en su sistema.

Igualmente, se require pip.

## Instalación
Para instalar y configurar el programa, siga estos pasos:

1. **Clonar el Repositorio**:
   Primero, clone el repositorio a su máquina local utilizando el siguiente comando:
   ```
   git clone https://github.com/migurd/chi-squared
   cd chi2-squared
   ```
2.  **Crear y Activar el Entorno Virtual**: Luego, cree y active un entorno virtual. Esto se hace de manera diferente en Windows y Linux/Mac.

#### En Windows:
```
python -m venv venv
venv\Scripts\activate
```
#### En Linux/Mac:
```
python3 -m venv venv
source venv/bin/activate
```
3. Instalar las Dependencias:
Con el entorno virtual activado, instale las dependencias necesarias ejecutando:

```
pip install -r requirements.txt
```

## Uso
Para ejecutar el programa, utilice el siguiente comando:
```
python main.py
```
### Carga de Datos Manual
El programa permite definir manualmente el número de ítems a ser considerados (con un máximo de 8). Los valores de los ítems pueden introducirse de manera aleatoria y/o manual.

### Carga de Datos Automatizada
Para una carga automatizada de datos, asegúrese de tener un archivo Excel, por ejemplo, PAN.XLS, con el nombre de los ítems y sus valores (0 y 1). El programa solicitará la ruta del archivo Excel para cargar los datos.

### Construcción de Tablas de Contingencia
El programa permite seleccionar 2 ítems para construir una tabla de contingencia, que es una matriz que muestra la frecuencia de las diferentes combinaciones de los valores de los dos ítems seleccionados.

### Cálculo de Valores de Confianza y Cobertura
El programa calculará y mostrará todos los valores de confianza y cobertura para las reglas de 2 ítems, proporcionando una medida de la precisión y la amplitud de las reglas generadas.

### Mostrar Factor de Dependencia
El programa también calculará y mostrará el Factor de Dependencia, una métrica que indica la fuerza de la relación entre los ítems seleccionados.

### Determinación de la Significancia del Valor de Dependencia
Finalmente, el programa realizará la Prueba Chi-Cuadrado para determinar la significancia del valor de dependencia a niveles de confianza del 95%, 99% y 99.99%. Los resultados se mostrarán al usuario.

### Archivo de Prueba
Para probar el programa, utilice el archivo PAN.XLS. Asegúrese de que el archivo esté en el formato correcto, con los nombres de los ítems y sus valores (0 y 1).
