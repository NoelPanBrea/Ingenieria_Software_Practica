from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, 
                            QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import joblib
from models.lineal_model import *
from sklearn.metrics import mean_squared_error, r2_score
from models.description import *
from ui.popup_handler import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui.popup_handler import InputDialog


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

        # Botón para realizar predicción (inicialmente oculto)
        self.predict_button = QPushButton("Realizar Predicción")
        self.predict_button.setVisible(False)  # Oculto inicialmente
        self.predict_button.clicked.connect(self.make_prediction)
        layout.addWidget(self.predict_button)

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

                # Mostrar el botón "Realizar Predicción"
                self.predict_button.setVisible(True)

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
        Saves the trained linear regression model to a file.
        The model data includes the formula, coefficients, intercept, description, 
        metrics (R², RMSE), and column information.
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


    def make_prediction(self):
        """
        Method to make predictions with the model.
        """
        if not self.model:
            QMessageBox.critical(self, "Error", "No se ha entrenado ningún modelo.")
            return

        if not self.input_columns:
            QMessageBox.critical(self, "Error", "No se han definido columnas de entrada.")
            return

        # Crear ventana emergente usando InputDialog
        input_window = InputDialog(
            self.input_columns,  # Lista de nombres de columnas de entrada
            "Introduzca los valores de las entradas",
            parent=self
        )
        input_window.exec()

        # Obtener los valores ingresados
        constants = input_window.get_inputs()

        # Validar los valores ingresados
        if not constants or any(value is None for value in constants):
            QMessageBox.warning(self, "Advertencia", "Debe proporcionar valores para todas las entradas.")
            return

        try:
            # Convertir los valores ingresados a flotantes
            numeric_data = [float(value) for value in constants]  # Conversión explícita
            data_to_predict = np.array([numeric_data])  # Convertir a un array NumPy con forma adecuada

            # Realizar la predicción
            prediction = self.model.predict(data_to_predict)[0]  # Obtener la predicción

            # Mostrar el resultado de la predicción
            QMessageBox.information(self, "Predicción", f"La predicción del modelo es:\n{self.output_column} = {prediction:.4f}")

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, introduzca solo valores numéricos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al realizar la predicción: {str(e)}")