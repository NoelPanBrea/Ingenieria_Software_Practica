from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, 
                            QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import joblib
from tabs.lineal_model_aux.class_LinealModel import *
from sklearn.metrics import mean_squared_error, r2_score
from tabs.lineal_model_aux.description import *
from tabs.data_aux.popup_handler import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class LinealModelTab(QWidget):
    def __init__(self, data, input_columns, output_column, parent=None):
        super().__init__(parent)
        self.model_description = ModelDescription()
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
        self.description_display = QLabel("Haz clic para añadir una descripción...")
        self.description_display.setStyleSheet("""
            QLabel {
                color: #4E342E;
                font-size: 15px;
                padding: 2px;
            }
        """)
        self.description_display.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.description_display.setMouseTracking(True)
        self.description_display.setCursor(Qt.PointingHandCursor)
        
        # Configurar campo de texto editable
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Escribe aquí la descripción del modelo...")
        self.description_input.setStyleSheet("""
            QLineEdit {
                font-size: 11px;
                padding: 2px;
            }
        """)
        self.description_input.hide()

        # Conectar eventos de interacción
        self.description_input.returnPressed.connect(self.save_description)
        self.description_input.focusOutEvent = self.on_focus_lost
        self.description_display.mousePressEvent = self.on_label_click

        # Cargar descripción desde la base de datos o archivo
        loaded_description = self.model_description.load_description()
        if loaded_description:
            self.description_display.setText(loaded_description)
        
        layout.addWidget(self.description_display)
        layout.addWidget(self.description_input)

        # Contenedor para la gráfica
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)
        self.graph_layout.setContentsMargins(0, 10, 0, 10)  # Margen para separar del resto
        layout.addWidget(self.graph_container)
        
        # Espaciador para empujar widgets hacia arriba
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.save_button = QPushButton("💾 Guardar Modelo")
        self.save_buton.clicked.connect(self.save_model)
        self.save_button.setVisible(False)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
    
    def create_model(self):
        # Eliminar cualquier gráfico existente, incluso si no se va a crear uno nuevo
        self.clear_previous_graph()

        if self.data is None or self.input_columns is None or self.output_column is None:
            QMessageBox.critical(self, "Error", "ADRIII EL ERROR ESTÁ EN LINEALMODELTAB")
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

    def on_label_click(self, event):
        """
        Activa el modo de edición cuando se hace clic en la descripción.
        """
        self.description_display.hide()
        current_text = self.description_display.text()
        
        # Limpiar el campo si tiene el texto por defecto
        if current_text == "Haz clic para añadir una descripción...":
            self.description_input.setText("")
        else:
            self.description_input.setText(current_text)
            
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
            self.model_description.save_description(description)  # Guardar en almacenamiento
        
        self.description_input.hide()
        self.description_display.show()

    # Método para obtener la descripción actual
    def get_current_description(self):
        """
        Retorna la descripción actual del modelo.
        """
        text = self.description_display.text()
        if text == "(Opcional) Haz clic para añadir una descripción...":
            return ""
        return text

    # Método para establecer una descripción 
    def set_description(self, description):
        """
        Establece una descripción.
        """
        if description:
            self.description_display.setText(description)
            self.model_description.save_description(description)
    
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
                "rmse": mean_squared_error(self.model.y, self.model.y_pred)
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

    def update_data(self, data, input_columns, output_column):
        """
        Actualiza los datos, columnas de entrada y columna de salida de la pestaña de modelo.
        """
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column