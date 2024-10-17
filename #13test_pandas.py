# Importar las bibliotecas necesarias
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Cargar los datos
# Reemplaza 'ruta_del_archivo.csv' con la ruta del archivo descargado en tu PC
ruta_archivo = 'C:\Users\ainho\OneDrive\Documentos\Prácticas\E.S\Ingenieria_Software_Practica\src\housing.csv'
datos = pd.read_csv(ruta_archivo)

# Verificar los datos cargados
print(datos.head())

# 2. Seleccionar las variables dependientes (X) e independientes (y)
# Supongamos que 'y' es la columna objetivo y todas las demás columnas son las características (X)
# Asegúrate de ajustar esto según tu archivo
X = datos.drop('y', axis=1)  # Características
y = datos['y']  # Objetivo

# 3. Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entrenar el modelo lineal
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# 5. Hacer predicciones con los datos de entrenamiento
y_pred_train = modelo.predict(X_train)

# 6. Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R²)
mse_train = mean_squared_error(y_train, y_pred_train)
r2_train = r2_score(y_train, y_pred_train)

# 7. Imprimir los resultados
print(f"Error cuadrático medio en el conjunto de entrenamiento: {mse_train}")
print(f"Coeficiente de determinación R² en el conjunto de entrenamiento: {r2_train}")

# Para el conjunto de prueba
y_pred_test = modelo.predict(X_test)
mse_test = mean_squared_error(y_test, y_pred_test)
r2_test = r2_score(y_test, y_pred_test)

print(f"\nError cuadrático medio en el conjunto de prueba: {mse_test}")
print(f"Coeficiente de determinación R² en el conjunto de prueba: {r2_test}")