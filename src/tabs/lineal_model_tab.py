# linear_model_tab.py
import pandas as pd
import joblib 
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from sklearn.metrics import root_mean_squared_error, r2_score

# Importar el modelo y la función gráfica de tus archivos
from tabs.lineal_model_aux.lineal_model import LinealModel, create_graphic
from tabs.data_aux.popup_handler import *

class LinearModelTab(QWidget):
    def __init__(self, data, input_columns, output_column):
        super().__init__()
        
        # Guardar datos y columnas
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = None

        # Inicializar la interfaz
        self.init_ui()

    def init_ui(self):
     """
     Configura la interfaz de usuario de la pestaña.
     """
     # Crear los elementos de la interfaz
     self.init_train_button()
     self.init_save_button()
     self.init_result_label()
     self.init_description_field()

     # Conectar eventos
     self.connect_signals()

     # Configurar el layout de la pestaña
     layout = QVBoxLayout()
    
     layout.addWidget(self.train_button)
     layout.addWidget(self.result_label)
     layout.addWidget(self.description_display)
     layout.addWidget(self.description_input)

     # Espaciador para empujar widgets hacia arriba
     layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

     # Crear un layout horizontal para el botón de guardar en la parte inferior derecha
     save_button_layout = QHBoxLayout()
     save_button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
     save_button_layout.addWidget(self.save_button)

     # Añadir el layout horizontal al layout principal
     layout.addLayout(save_button_layout)

     self.setLayout(layout)

    def init_train_button(self):
        """
        Inicializa el botón de entrenamiento del modelo.
        """
        self.train_button = QPushButton("Entrenar Modelo Lineal")

    def init_result_label(self):
        """
        Inicializa la etiqueta de resultados.
        """
        self.result_label = QLabel("Presiona el botón para entrenar el modelo.")
    
    def init_save_button(self):
        """
        Inicializa el botón de guardado del modelo.
        """
        self.save_button = QPushButton("💾 Guardar Modelo")
        self.save_button.setVisible(False)

    def init_description_field(self):
        """
        Configura el campo de descripción editable.
        """
        self.description_display = QLabel("Haz clic para añadir una descripción...")
        self.description_display.setStyleSheet("""
            QLabel {
                color: #4E342E;
                font-size: 15px;
                padding: 2px;
            }
        """)
        self.description_display.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.description_display.setCursor(Qt.PointingHandCursor)
        
        # Campo de texto para editar la descripción
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Escribe aquí la descripción del modelo...")
        self.description_input.setStyleSheet("""
            QLineEdit {
                font-size: 11px;
                padding: 2px;
            }
        """)
        self.description_input.hide()  # Ocultar inicialmente el campo de edición

    def connect_signals(self):
        """
        Conecta los eventos de la interfaz.
        """
        # Conectar el botón de entrenamiento al método correspondiente
        self.train_button.clicked.connect(self.train_model)
        
        # Conectar el botón de guardado de modelos
        self.save_button.clicked.connect(self.save_model)

        # Conectar eventos para el campo de descripción
        self.description_display.mousePressEvent = self.on_label_click
        self.description_input.returnPressed.connect(self.save_description)
        self.description_input.focusOutEvent = self.on_focus_lost

    def train_model(self):
        """
        Entrena el modelo lineal y muestra los resultados en la interfaz.
        """
        # Crear y ajustar el modelo lineal
        self.model = LinealModel(self.data, self.input_columns, self.output_column)
        self.model.fit()
        
        # Obtener métricas del modelo
        mse = root_mean_squared_error(self.model.y, self.model.y_pred)
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
        
        self.save_button.setVisible(True)
    def on_label_click(self, event):
        """
        Activa el modo de edición cuando se hace clic en la descripción.
        """
        self.description_display.hide()
        self.description_input.setText(self.description_display.text())
        self.description_input.show()
        self.description_input.setFocus()

    def on_focus_lost(self, event):
        """
        Guarda la descripción cuando el campo de texto pierde el foco.
        """
        self.save_description()
        QLineEdit.focusOutEvent(self.description_input, event)

    def save_description(self):
        """
        Guarda la descripción y vuelve al modo de visualización.
        """
        description = self.description_input.text()
        
        if not description:
            self.description_display.setText("Haz clic para añadir una descripción...")
        else:
            self.description_display.setText(description)
        
        self.description_input.hide()
        self.description_display.show()

    def save_model(self):
        """
        Guarda el modelo lineal.
        """
        if self.model is None:
            show_error('⚠ Debe primero entrenar el modelo ⚠')
            return

        # Datos del modelo a guardar
        model_data = {
            "formula": (self.model.formula),                          # Fórmula del modelo
            "coefficients": self.model.coef_.tolist(),                # Coeficientes del modelo
            "intercept": self.model.intercept_,                      # Intersección del modelo
            "description": self.description_display.text(),         # Descripción del modelo
            "metrics": {
                "r2_score": r2_score(self.model.y, self.model.y_pred),
                "rmse": root_mean_squared_error(self.model.y, self.model.y_pred)
            },
            "columns": {
                "input": self.input_columns,
                "output": self.output_column
            }
        }
    
        try:
         joblib.dump(model_data, "linear_model_data.joblib")
        
         show_message("✅ ¡Modelo guardado exitosamente! 😃")
         
        except Exception as e:
            show_error(f"⚠ Error al guardar el modelo: {str(e)} ⚠")
            