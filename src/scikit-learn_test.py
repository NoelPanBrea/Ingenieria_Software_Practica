# Importar librerías necesarias
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Cargar un dataset proporcionado por scikit-learn
file_path = "C:\\Users\\Usuario\\Downloads\\housing.csv"
housing_data = pd.read_csv(file_path)

x = housing_data[['latitude']].values # Variables independientes
y = housing_data['population'].values  # Variable dependiente

# Dividir los datos en conjunto de entrenamiento y prueba (80% para entrenamiento y 20% para prueba)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Crear el modelo de regresión lineal
modelo = LinearRegression()

# Entrenar el modelo con los datos de entrenamiento
modelo.fit(x_train, y_train)

# Realizar predicciones con el conjunto de prueba
y_pred = modelo.predict(x_test)

# Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R²)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Mostrar los resultados
print(f"Error Cuadrático Medio (MSE): {mse}")
print(f"Coeficiente de Determinación (R²): {r2}")


# Graficamos los datos estandarizados
plt.scatter(x, y)
# Graficamos la linea de regresion ajustada
plt.plot(x, modelo.predict(x), color='red')

plt.xlabel("Latitud (RM)")
plt.ylabel("Población (MEDV)")

plt.show()