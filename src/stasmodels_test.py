# Importamos las librerías necesarias
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Cargar el dataset de ejemplo (diabetes)
file_path = "C:\\Users\\Usuario\\Downloads\\housing.csv"
housing_data = pd.read_csv(file_path)

x = housing_data[['latitude']].values # Variables independientes
y = housing_data['population'].values  # Variable dependiente

# Dividir los datos en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Statsmodels requiere que agreguemos explícitamente una constante a las variables independientes (intercepto)
x_train = sm.add_constant(x_train)  # Agregamos la constante
x_test = sm.add_constant(x_test)    # Hacemos lo mismo con el conjunto de prueba

# Ajustar el modelo usando OLS (Ordinary Least Squares = Mínimos Cuadrados Ordinarios)
modelo = sm.OLS(y_train, x_train)  # Creamos el modelo
resultados = modelo.fit()          # Ajustamos el modelo

# Imprimir el resumen del modelo
print(resultados.summary())

# Predecir valores usando el conjunto de prueba
y_pred = resultados.predict(x_test)

# Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R²)
from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Mostrar resultados
print(f"Error Cuadrático Medio (MSE): {mse}")
print(f"Coeficiente de Determinación (R²): {r2}")

# Agregar la constante al conjunto original de X
x_const = sm.add_constant(x)

# Graficamos los datos estandarizados
plt.scatter(x, y)
# Graficamos la linea de regresion ajustada
plt.plot(x, resultados.predict(x_const), color='red')

plt.xlabel("Latitud (RM)")
plt.ylabel("Población (MEDV)")

plt.show()