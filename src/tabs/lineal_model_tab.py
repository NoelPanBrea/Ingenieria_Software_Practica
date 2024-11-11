from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, 
                            QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import joblib
from tabs.lineal_model_aux.class_LinealModel import *
from sklearn.metrics import mean_squared_error, r2_score
from tabs.lineal_model_aux.description import *
from tabs.data_aux.common_aux.popup_handler import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class LinealModelTab(QWidget):
    def __init__(self, data, input_columns, output_column, parent=None):
        super().__init__(parent)
        self.model_description = ModelDescription(self)
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = None
        self.canvas = None  # Referencia para el gráfico
        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Botón para crear el modelo
        self.create_model_button = QPushButton("Crear Modelo de Regresión Lineal")
        self.create_model_button.clicked.connect(self.create_model)
        layout.addWidget(self.create_model_button)

        # Etiquetas para mostrar fórmula y métricas
        self.formula_label = QLabel("Fórmula del Modelo:")
        self.r2_label = QLabel("R²: ")
        self.mse_label = QLabel("ECM: ")
        
        # Añadir al layout
        layout.addWidget(self.formula_label)
        layout.addWidget(self.r2_label)
        layout.addWidget(self.mse_label)

        # Configurar etiqueta para mostrar la descripción
        self.model_description.add_to_layout(layout)
        # Contenedor para la gráfica
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)
        self.graph_layout.setContentsMargins(0, 10, 0, 10)  # Margen para separar del resto
        layout.addWidget(self.graph_container)
        
        # Espaciador para empujar widgets hacia arriba
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.save_button = QPushButton("💾 Guardar Modelo")
        self.save_button.clicked.connect(self.save_model)
        self.save_button.setVisible(False)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
    
    def create_model(self):
        # Eliminar cualquier gráfico existente, incluso si no se va a crear uno nuevo
        self.save_button.setVisible(True)
        self.clear_previous_graph()

        if self.data is None or self.input_columns is None or self.output_column is None:
            QMessageBox.critical(self, "Error", "ERROR")
        else:
            try:
                self.canvas = None  # Restablecer la referencia a None
                # Crear y ajustar el modelo
                self.model = LinealModel(self.data, self.input_columns, self.output_column)
                self.model.fit()

                # Actualizar la interfaz con la fórmula y métricas
                self.formula_label.setText(f"Fórmula del Modelo: {self.model.formula}")
                self.r2_label.setText(f"R²: {self.model.r2_:.4f}")
                self.mse_label.setText(f"ECM: {self.model.mse_:.4f}")

                # Graficar si es posible
                if len(self.model.input_columns) == 1:
                    self.plot_graph()
                else:
                    QMessageBox.information(self, 
                                            "Atención", "No se puede crear una gráfica, debido a que la regresión lineal es múltiple, no simple.")


                # Confirmación de éxito
                QMessageBox.information(self, "Éxito", "El modelo de regresión lineal ha sido creado exitosamente.")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear el modelo lineal: {str(e)}")

    def clear_previous_graph(self):
        # Verificar si existe una gráfica previa y eliminarla
        if self.canvas:
            self.canvas.setParent(None)
            self.canvas.deleteLater()
            self.canvas = None  # Restablecer la referencia a None

    def plot_graph(self):
        
        # Crear la figura y el canvas
        fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        # Dibujar la gráfica de dispersión y la línea de regresión
        ax.scatter(self.model.x, self.model.y, label="Datos Reales")
        ax.plot(self.model.x, self.model.y_pred, color='red', label="Línea de Regresión")
        ax.set_xlabel(self.model.input_columns[0])
        ax.set_ylabel(self.model.output_column)
        ax.legend()

        # Añadir el canvas al contenedor de la gráfica
        self.graph_layout.addWidget(self.canvas)
        self.canvas.draw()


    
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
            "description": self.model_description.get_description(),         # Descripción del modelo
            "metrics": {
                "r2_score": r2_score(self.model.y, self.model.y_pred),
                "rmse": mean_squared_error(self.model.y, self.model.y_pred)
            },
            "columns": {
                "input": self.input_columns,
                "output": self.output_column
            }
        }
    
        try:
         file_path = save_file_dialog()
         joblib.dump(model_data, file_path)
        
         show_message("✅ ¡Modelo guardado exitosamente! 😃")
         
        except Exception as e:
            show_error(f"⚠ Error al guardar el modelo: {str(e)} ⚠")

    def update_data(self, data, input_columns, output_column):
        """
        Actualiza los datos, columnas de entrada y columna de salida de la pestaña de modelo.
        """
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column