from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, 
    QSpacerItem, QHBoxLayout, QApplication, QGroupBox)
from PyQt5.QtCore import Qt
import joblib
import numpy as np
from models.lineal_model import LinealModel
from sklearn.metrics import mean_squared_error, r2_score
from models.description import *
from ui.popup_handler import (show_error, show_message, show_warning, save_file_dialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LinealModelTab(QWidget):
    tab_list = []

    def __init__(self, data=None, input_columns=None, output_column=None, loaded_model=None, parent=None):
        super().__init__(parent)
        LinealModelTab.tab_list.append(self)
        self.model_description = ModelDescription(self)
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = None
        self.canvas = None
        self.loaded_model = loaded_model
        self.setup_ui()

        if loaded_model:
            self.initialize_from_loaded_model(loaded_model)
        else:
            self.initialize_for_new_model()

    def setup_ui(self):
        """Configura la interfaz de usuario con una mejor organización"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. Grupo superior - Creación del modelo
        if not self.loaded_model:
            model_creation_group = QGroupBox("Creación del Modelo")
            model_creation_group.setFixedHeight(100)
            model_creation_layout = QHBoxLayout()
            model_creation_layout.setContentsMargins(0, 0, 0, 0)
            
            self.create_model_button = QPushButton("Crear Modelo de Regresión Lineal")
            self.create_model_button.setObjectName("create_model_button")
            self.create_model_button.setFixedSize(350, 50)
            self.create_model_button.clicked.connect(self.create_model)
            
            
            model_creation_layout.addWidget(self.create_model_button, Qt.AlignCenter)
            model_creation_group.setLayout(model_creation_layout)
            main_layout.addWidget(model_creation_group)

        # 2. Grupo de información del modelo
        model_info_group = QGroupBox("Información del Modelo")
        model_info_layout = QVBoxLayout()
        model_info_layout.setSpacing(5)
        model_info_layout.setContentsMargins(10, 10, 10, 10)
        
        self.formula_label = QLabel("Fórmula del Modelo:")
        self.formula_label.setObjectName("formula_label")
        self.r2_label = QLabel("R²: ")
        self.r2_label.setObjectName("r2_label")
        self.mse_label = QLabel("ECM: ")
        self.mse_label.setObjectName("mse_label")
        
        model_info_layout.addWidget(self.formula_label)
        model_info_layout.addWidget(self.r2_label)
        model_info_layout.addWidget(self.mse_label)
        
        self.model_description.add_to_layout(model_info_layout)
        model_info_group.setLayout(model_info_layout)
        main_layout.addWidget(model_info_group)

        # 3. Layout horizontal para contener visualización y predicción lado a lado
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        # Contenedor izquierdo para predicción y botón guardar
        left_container = QVBoxLayout()
        left_container.setSpacing(5)

        # Grupo de predicción
        prediction_group = QGroupBox("Predicción")
        prediction_group.setMaximumWidth(400)
        prediction_layout = QVBoxLayout()
        prediction_layout.setSpacing(0)
        prediction_layout.setContentsMargins(10, 5, 10, 10)
        
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout(self.input_container)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setSpacing(0)
        self.input_widgets = []
        prediction_layout.addWidget(self.input_container)
        
        self.prediction_label = QLabel()
        self.prediction_label.setObjectName("prediction_label")
        self.prediction_label.setVisible(False)
        prediction_layout.addWidget(self.prediction_label)
        
        # Botón de predicción
        predict_button_container = QHBoxLayout()
        predict_button_container.setContentsMargins(10, 20, 10, 20)  # Márgenes amplios
        self.predict_button = QPushButton("Realizar Predicción")
        self.predict_button.setFixedHeight(50)
        self.predict_button.setVisible(False)
        self.predict_button.clicked.connect(self.make_prediction)
        predict_button_container.addWidget(self.predict_button)
        prediction_layout.addLayout(predict_button_container)

        prediction_group.setLayout(prediction_layout)
        left_container.addWidget(prediction_group)
        
        # Botón guardar debajo del grupo de predicción
        save_button_container = QHBoxLayout()
        save_button_container.setContentsMargins(10, 20, 10, 20)  # Márgenes amplios
        self.save_button = QPushButton("💾 Guardar Modelo")
        self.save_button.setFixedHeight(50)
        self.save_button.clicked.connect(self.save_model)
        self.save_button.setVisible(False)
        save_button_container.addWidget(self.save_button)
        left_container.addLayout(save_button_container)
        
        # Añadir contenedor izquierdo al layout horizontal
        bottom_layout.addLayout(left_container)

        # Grupo de visualización (derecha)
        visualization_group = QGroupBox("Visualización")
        visualization_layout = QVBoxLayout()
        visualization_layout.setContentsMargins(10, 10, 10, 10)
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        visualization_layout.addWidget(self.graph_container)
        visualization_group.setLayout(visualization_layout)
        bottom_layout.addWidget(visualization_group)

        # Ajustar proporciones del espacio
        prediction_group.setMinimumWidth(300)
        visualization_group.setMinimumWidth(500)

        # Añadir el layout horizontal al layout principal
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def setup_model_display(self, model_data):
        """
        Método unificado para mostrar datos del modelo, ya sea nuevo o cargado
        """
        try:
            # Configurar fórmula y métricas
            self.formula_label.setText(f"Fórmula del Modelo: {model_data['formula']}")
            self.r2_label.setText(f"R²: {float(model_data['metrics']['r2_score']):.4f}")
            self.mse_label.setText(f"ECM: {float(model_data['metrics']['rmse']):.4f}")
            
            # Configurar descripción si existe
            if 'description' in model_data:
                self.model_description.set_description(model_data['description'])
            
            # Configurar campos de entrada para predicción
            self.input_columns = model_data['columns']['input']
            self.output_column = model_data['columns']['output']
            self.create_prediction_inputs()
            
            # Mostrar botones de predicción y guardado
            self.predict_button.setVisible(True)
            self.save_button.setVisible(True)

            # Actualizar UI
            self.update()
            QApplication.processEvents()

        except Exception as e:
            show_error(f"Error al mostrar datos del modelo: {str(e)}", self)
            raise

    def initialize_from_loaded_model(self, loaded_model):
        """Inicializa la pestaña con un modelo cargado"""
        try:
            # Configurar modelo
            self.model = LinealModel(None, 
                                loaded_model['columns']['input'],
                                loaded_model['columns']['output'])
            self.model.coef_ = np.array(loaded_model['coefficients'])
            self.model.intercept_ = float(loaded_model['intercept'])
            self.model.formula = loaded_model['formula']
            
            # Mostrar datos usando el método unificado
            self.setup_model_display({
                'formula': loaded_model['formula'],
                'metrics': loaded_model['metrics'],
                'description': loaded_model['description'],
                'columns': loaded_model['columns']
            })
            
        except Exception as e:
            show_error(f"Error al inicializar el modelo cargado: {str(e)}", self)
            raise

    def initialize_for_new_model(self):
        """Inicializa la pestaña para un nuevo modelo"""
        self.create_prediction_inputs()

    def create_prediction_inputs(self):
        """Crea los campos de entrada para predicciones con espaciado mínimo"""
        for widget in self.input_widgets:
            widget[0].setParent(None)
            widget[1].setParent(None)
        self.input_widgets.clear()
        
        if self.input_columns:
            for column in self.input_columns:
                # Crear un widget contenedor para cada par label-input
                container = QWidget()
                container_layout = QVBoxLayout(container)
                container_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
                container_layout.setSpacing(0)  # Sin espacio entre elementos
                
                label = QLabel(f"{column}:")
                label.setFixedHeight(25)  # Altura fija para el label
                
                line_edit = QLineEdit()
                line_edit.setFixedHeight(30)  # Altura fija para el input
                line_edit.setFixedWidth(300)
                
                container_layout.addWidget(label)
                container_layout.addWidget(line_edit)
                
                self.input_widgets.append((label, line_edit))
                self.input_layout.addWidget(container)
                
                # Establecer visibilidad
                label.setVisible(self.model is not None)
                line_edit.setVisible(self.model is not None)
                
            # Añadir un espaciador al final
            self.input_layout.addStretch()

    def create_model(self):
        """Crea un nuevo modelo de regresión lineal"""
        self.clear_previous_graph()
        try:
            # Crear y ajustar el modelo
            self.model = LinealModel(self.data, self.input_columns, self.output_column)
            self.model.fit()

            # Mostrar datos
            self.setup_model_display({
                'formula': self.model.formula,
                'metrics': {
                    'r2_score': self.model.r2_,
                    'rmse': self.model.mse_
                },
                'description': self.model_description.get_description(),
                'columns': {
                    'input': self.input_columns,
                    'output': self.output_column
                }
            })

            # Graficar si es posible
            if len(self.model.input_columns) == 1:
                self.plot_graph()
            else:
                show_message(
                    "No se puede crear una gráfica, debido a que la regresión lineal es múltiple, no simple.",
                    self
                )

            show_message("El modelo de regresión lineal ha sido creado exitosamente.", self)

        except Exception as e:
            show_error(f"Error al crear el modelo lineal: {str(e)}", self)

    def clear_previous_graph(self):
        # Verificar si existe una gráfica previa y eliminarla
        if self.canvas:
            self.canvas.setParent(None)
            self.canvas.deleteLater()
            self.canvas = None  # Restablecer la referencia a None
            
    def plot_graph(self):
        """Crea y muestra la gráfica del modelo"""
        if not hasattr(self.model, 'x') or not hasattr(self.model, 'y'):
            return      
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
        if not self.model:
            show_error('⚠ Debe primero entrenar o cargar un modelo ⚠')
            return

        try:
            # Para modelos cargados, usar las métricas existentes
            if hasattr(self, 'loaded_model') and self.loaded_model is not None:
                metrics = self.loaded_model['metrics']
            else:
                # Para modelos nuevos, calcular métricas
                metrics = {
                    'r2_score': float(self.model.r2_) if hasattr(self.model, 'r2_') 
                            else r2_score(self.model.y, self.model.y_pred),
                    'rmse': float(self.model.mse_) if hasattr(self.model, 'mse_') 
                        else mean_squared_error(self.model.y, self.model.y_pred)
                }

            # Preparar datos del modelo
            model_data = {
                'formula': self.model.formula,
                'coefficients': self.model.coef_.tolist(),
                'intercept': float(self.model.intercept_),
                'description': self.model_description.get_description(),
                'metrics': metrics,
                'columns': {
                    'input': self.input_columns,
                    'output': self.output_column
                }
            }
        
            # Guardar modelo
            file_path = save_file_dialog()
            if file_path:
                joblib.dump(model_data, file_path)
                show_message("✅ ¡Modelo guardado exitosamente! 😃")
         
        except Exception as e:
            show_error(f"⚠ Error al guardar el modelo: {str(e)} ⚠")


    def make_prediction(self):
        """
        Method to make predictions with the model.
        """
        if not self.model:
            show_error("No hay un modelo disponible para realizar predicciones.", self)
            return

        # Mostrar todos los QLabel y QLineEdit asociados
        for label, line_edit in self.input_widgets:
            label.setVisible(True)
            line_edit.setVisible(True)

        # Actualizar el layout para reflejar la visibilidad de los campos
        self.layout().update()

        # Obtener los valores ingresados en los QLineEdits
        input_values = []
        for label, line_edit in self.input_widgets:
            value = line_edit.text()
            if not value:
                show_warning("Debe rellenar todas las celdas para realizar predicción.", self)
                return None
                
            try:
                input_values.append(float(value))
            except ValueError:
                show_error(f"El valor para {label.text()} debe ser numérico.", self)
                return None

        try:
            # Realizar la predicción
            prediction = self.model.intercept_
            for i in range(len(input_values)):
                prediction += self.model.coef_[i] * input_values[i]
        

            # Actualizar QLabel para mostrar el resultado
            self.prediction_label.setText(f"Resultado de la Predicción:\n{self.output_column} = {prediction:.4f}")
            self.prediction_label.setVisible(True)  # Mostrar el QLabel

        except ValueError:
            show_error("Por favor, introduzca solo valores numéricos.", self)

    
    

    