# Importamos las librerías necesarias
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score

# Cargar el dataset de ejemplo (housing)
file_path = "C:\\Users\\Usuario\\Downloads\\housing.csv"
housing_data = pd.read_csv(file_path)

# Variables independientes (X) y dependientes (y)
x = housing_data[['latitude']].values  # Variable independiente
y = housing_data['population'].values  # Variable dependiente

# Statsmodels requiere que agreguemos explícitamente una constante a las variables independientes (intercepto)
x = sm.add_constant(x)  # Agregamos la constante (intercepto)

# Ajustar el modelo usando OLS (Ordinary Least Squares = Mínimos Cuadrados Ordinarios)
modelo = sm.OLS(y, x)  # Creamos el modelo
resultados = modelo.fit()  # Ajustamos el modelo

# Imprimir el resumen del modelo
print(resultados.summary())

# Predecir valores usando el conjunto de entrenamiento
y_pred = resultados.predict(x)

# Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R²)
mse = root_mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

# Mostrar resultados
print(f"Error Cuadrático Medio (MSE): {mse}")
print(f"Coeficiente de Determinación (R²): {r2}")

# Graficar los datos originales y la línea de regresión ajustada
plt.scatter(housing_data['latitude'], y, label="Datos Reales")
plt.plot(housing_data['latitude'], y_pred, color='red', label="Línea de Regresión")

plt.xlabel("Latitud")
plt.ylabel("Población")
plt.legend()
plt.show()