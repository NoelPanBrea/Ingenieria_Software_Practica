import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score


def create_lineal_model(data, input_columns, output_column):
    x = data[input_columns].values # Variables independientes
    y = data[output_column].values  # Variable dependiente

    # Crear el modelo de regresión lineal
    modelo = LinearRegression()

    # Entrenar el modelo con los datos de entrenamiento
    resultados = modelo.fit(x, y)

    # Predecir valores usando el conjunto de entrenamiento
    y_pred = resultados.predict(x)

    # Graficar los datos originales y la línea de regresión ajustada (si hay una sola variable independiente)
    if len(input_columns) == 1:  # Solo graficar si hay una variable independiente
        plt.scatter(x, y, label="Datos Reales")
        plt.plot(x, y_pred, color='red', label="Línea de Regresión")

        # Etiquetas de los ejes
        plt.xlabel(input_columns)  # Nombre de la variable independiente
        plt.ylabel(output_column)  # Nombre de la variable dependiente
        plt.legend()
        plt.show()
    else:
        print("No se puede graficar cuando hay más de una variable independiente.")

    # Calcula la fórmula de la regresión
    coef = modelo.coef_
    intercept = modelo.intercept_
    
    formula = f"{output_column} = {intercept:.2f}"
    for i, col in enumerate(input_columns):
        formula += f" + ({coef[i]:.2f} * {col})"
        
    print(formula)

    # Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R²)
    mse = root_mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    print(f"Error Cuadrático Medio (MSE): {mse}")
    print(f"Coeficiente de Determinación (R²): {r2}")

