import pandas as pd
import numpy as np

# Supongamos que tenemos un DataFrame con datos de ejemplo
data = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],  # Tamaño de la casa
    'Y': [2, 4, 5, 4, 5]   # Precio de la casa
})

# Calcular las medias de X y Y
X_mean = data['X'].mean()
Y_mean = data['Y'].mean()

# Calcular la pendiente (w)
data['XY_cov'] = (data['X'] - X_mean) * (data['Y'] - Y_mean)
data['X_var'] = (data['X'] - X_mean) ** 2
w = data['XY_cov'].sum() / data['X_var'].sum()

# Calcular el intercepto (b)
b = Y_mean - w * X_mean

print(f"Pendiente (w): {w}")
print(f"Intercepto (b): {b}")

# Hacer predicciones usando la fórmula Y = wX + b
data['predicciones'] = w * data['X'] + b

# Mostrar los resultados
print(data[['X', 'Y', 'predicciones']])

# Calcular el MSE (Error Cuadrático Medio)
mse = ((data['Y'] - data['predicciones']) ** 2).mean()
print(f"Error Cuadrático Medio (MSE): {mse}")

# Calcular el R² (Coeficiente de Determinación)
ss_res = ((data['Y'] - data['predicciones']) ** 2).sum()  # Suma de los cuadrados de los residuos
ss_tot = ((data['Y'] - Y_mean) ** 2).sum()  # Suma total de los cuadrados
r2 = 1 - (ss_res / ss_tot)
print(f"Coeficiente de Determinación (R²): {r2}")
