import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score
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
        self.x = self.data[input_columns].values
        self.y = self.data[output_column].values
        self.model = LinearRegression()
        self.coef_ = None
        self.intercept_ = None
        self.y_pred = None
        self.mse_ = None
        self.r2_ = None
        self.formula = None

    # Ajusta el modelo lineal
    def fit(self):
        self.model.fit(self.x, self.y)
        self.coef_ = self.model.coef_
        self.intercept_ = self.model.intercept_
        self.predict()
        # self.plot()
        self.evaluate()
        self.calc_formula()

    def predict(self):
        self.y_pred = self.model.predict(self.x)
        return self.y_pred

    # Crea la gráfica
    # def plot(self):
        if len(self.input_columns) == 1:
            create_graphic(self.x, self.y, self.y_pred, self.input_columns, self.output_column)
        else:
            print("No se puede graficar cuando hay más de una variable independiente.")

    # Calcula coeficientes de errores
    def evaluate(self):      
        self.mse_ = root_mean_squared_error(self.y, self.y_pred)
        self.r2_ = r2_score(self.y, self.y_pred)
        
        print(f"Error Cuadrático Medio (MSE): {self.mse_}")
        print(f"Coeficiente de Determinación (R²): {self.r2_}")

    # Crea la fórmula de la regresión lineal
    def calc_formula(self):
        self.formula = f"{self.output_column} = {self.intercept_:.2f}"
        for i, col in enumerate(self.input_columns):
            self.formula += f" + ({self.coef_[i]:.2f} * {col})"


# Uso de la clase
if __name__ == '__main__':
    file_path = "C:\\Users\\Usuario\\Downloads\\housing.csv"
    data = pd.read_csv(file_path)
    input_columns = ['latitude', 'longitude']
    output_column = 'population'
    
    model = LinealModel(data, input_columns, output_column)
    model.fit()
    print(model.formula)









