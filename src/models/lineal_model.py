import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Función para crear la gráfica
def create_graphic(x, y, y_pred, input_columns, output_column):
    plt.scatter(x, y, label="Datos Reales")
    plt.plot(x, y_pred, color='red', label="Línea de Regresión")
    plt.xlabel(input_columns[0])
    plt.ylabel(output_column)
    plt.legend()
    plt.show()

class LinealModel:
    def __init__(self, data, input_columns, output_column):
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.x = None if data is None else self.data[input_columns].values
        self.y = None if data is None else self.data[output_column].values
        self.model = LinearRegression()
        self.coef_ = None
        self.intercept_ = None
        self.y_pred = None  # Inicializamos como None
        self.mse_ = None
        self.r2_ = None
        self.formula = None

    def set_model_params(self, coefficients, intercept, formula):
        """Método nuevo para establecer parámetros de un modelo cargado"""
        self.coef_ = coefficients
        self.intercept_ = intercept
        self.formula = formula
        return self

    # Ajusta el modelo lineal
    def fit(self):
        self.model.fit(self.x, self.y)
        self.coef_ = self.model.coef_
        self.intercept_ = self.model.intercept_

        # Aseguramos que se realice la predicción con los datos de entrenamiento
        self.y_pred = self.predict(self.x)  # Usamos el método predict
        self.evaluate()
        self.calc_formula()

    def predict(self, data_to_predict=None):
        """
        Predice valores usando el modelo ajustado.
        Si no se proporciona `data_to_predict`, usa los datos de entrenamiento.
        """
        if data_to_predict is None:
            data_to_predict = self.x  # Usa los datos de entrenamiento si no se especifican otros

        # Realizamos la predicción
        return self.model.predict(data_to_predict)

    # Calcula coeficientes de errores
    def evaluate(self):      
        # Verificamos que self.y_pred esté correctamente definido como un array
        if self.y_pred is None:
            raise ValueError("Predicciones no generadas. Asegúrate de llamar a 'fit' antes de evaluar.")
        self.mse_ = mean_squared_error(self.y, self.y_pred)
        self.r2_ = r2_score(self.y, self.y_pred)

    # Crea la fórmula de la regresión lineal
    def calc_formula(self):
        self.formula = f"{self.output_column} = {self.intercept_:.2f}"
        for i, col in enumerate(self.input_columns):
            self.formula += f" + ({self.coef_[i]:.2f} * {col})"