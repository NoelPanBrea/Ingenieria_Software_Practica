# linear_model_tab.py
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from sklearn.metrics import mean_squared_error, r2_score

# Importar el modelo y la función gráfica de tus archivos
from tabs.lineal_model_aux.linear_model import LinealModel, create_graphic


class LinearModelTab(QWidget):
    def __init__(self, data, input_columns, output_column):
        super().__init__()
        
        # Guardar datos y columnas
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = None

        # Crear la interfaz de la pestaña
        self.train_button = QPushButton("Entrenar Modelo Lineal")
        self.result_label = QLabel("Presiona el botón para entrenar el modelo.")
        
        # Conectar el botón a la función de entrenamiento
        self.train_button.clicked.connect(self.train_model)

        # Layout de la pestaña
        layout = QVBoxLayout()
        layout.addWidget(self.train_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def train_model(self):
        # Crear y ajustar el modelo lineal
        self.model = LinealModel(self.data, self.input_columns, self.output_column)
        self.model.fit()
        
        # Obtener métricas del modelo
        mse = mean_squared_error(self.model.y, self.model.y_pred)
        r2 = r2_score(self.model.y, self.model.y_pred)

        # Mostrar las métricas en la interfaz
        self.result_label.setText(
            f"Modelo entrenado.\nError cuadrático medio: {mse:.2f}\nCoeficiente de determinación (R²): {r2:.2f}\nFórmula: {self.model.formula}"
        )

        # Graficar el modelo si solo hay una variable independiente
        if len(self.input_columns) == 1:
            create_graphic(self.model.x, self.model.y, self.model.y_pred, self.input_columns, self.output_column)
        else:
            print("No se puede graficar con múltiples variables independientes.")
