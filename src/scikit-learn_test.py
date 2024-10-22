# Importar librerías necesarias
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score

# Cargar un dataset proporcionado por scikit-learn
file_path = "C:\\Users\\Usuario\\Downloads\\housing.csv"
housing_data = pd.read_csv(file_path)

x = housing_data[['latitude']].values # Variables independientes
y = housing_data['population'].values  # Variable dependiente

# Crear el modelo de regresión lineal
modelo = LinearRegression()

# Entrenar el modelo con los datos de entrenamiento
resultados = modelo.fit(x, y)

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