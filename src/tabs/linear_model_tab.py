from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, 
    QSpacerItem, QHBoxLayout, QApplication, QGroupBox, QScrollArea, QFrame)
import joblib
import numpy as np
from models.linear_model import LinearModel
from sklearn.metrics import mean_squared_error, r2_score
from models.description import *
from ui.popup_handler import (show_error, show_message, 
    show_warning, save_file_dialog)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib import style
style.use('fivethirtyeight')


class LinearModelTab(QWidget):
    """
    UI Tab for managing linear regression models.

    Handles the creation, visualization, saving, and prediction of linear regression models.
    Allows users to load a pre-trained model or create a new one from input data.

    Attributes
    ----------
    tab_list : list
        Keeps track of all instances of this class.
    model_description : ModelDescription
        Handles the description of the model.
    data : Optional[np.ndarray]
        Input dataset.
    input_columns : Optional[list[str]]
        Names of the input columns.
    output_column : Optional[str]
        Name of the output column.
    model : Optional[LinearModel]
        Instance of the trained linear regression model.
    canvas : Optional[FigureCanvasQTAgg]
        Canvas for displaying plots.
    loaded_model : Optional[dict]
        Dictionary containing the loaded model's information.
    """

    tab_list = []

    def __init__(self, data=None, input_columns=None, output_column=None, loaded_model=None, parent=None):
        """
        Initializes the LinearModelTab.

        Parameters
        ----------
        data : Optional[np.ndarray]
            The input dataset.
        input_columns : Optional[list[str]]
            Names of the input columns.
        output_column : Optional[str]
            Name of the output column.
        loaded_model : Optional[dict]
            Pre-trained model to be loaded into the tab.
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)
        LinearModelTab.tab_list.append(self)
        self.model_description = ModelDescription(self)
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = None
        self.canvas = None  # Graph canvas reference
        self.loaded_model = loaded_model
        self.input_widgets = []
        self.setup_ui()

        # Initialize based on whether a model is loaded or a new one is being created
        if loaded_model:
            self.initialize_from_loaded_model(loaded_model)
        else:
            self.initialize_for_new_model()

    def setup_ui(self):
        """
        Sets up the UI components for the tab, including buttons, labels, and layouts.
        """
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Group 1: Model creation (only shown if no model is loaded)
        if not self.loaded_model:
            model_creation_group = QGroupBox("Creación del Modelo")
            model_creation_group.setFixedHeight(100)
            model_creation_layout = QHBoxLayout()
            model_creation_layout.setContentsMargins(0, 0, 0, 0)
            
            # Button to create a new model
            self.create_model_button = QPushButton("Crear Modelo de Regresión Lineal")
            self.create_model_button.setObjectName("create_model_button")
            self.create_model_button.setFixedSize(350, 50)
            self.create_model_button.clicked.connect(self.create_model)
            

            model_creation_layout.addWidget(self.create_model_button, Qt.AlignCenter)
            model_creation_group.setLayout(model_creation_layout)
            main_layout.addWidget(model_creation_group)

        # Create horizontal layout for main content
        content_layout = QHBoxLayout()
        
        # Left side container with vertical layout
        left_container = QVBoxLayout()
        
        # Group 2: Model information
        model_info_group = QGroupBox("Información del Modelo")
        model_info_layout = QVBoxLayout()
        model_info_layout.setSpacing(5)
        model_info_layout.setContentsMargins(10, 10, 10, 10)
        
        # Labels for formula and metrics
        self.formula_label = QLabel("Fórmula del Modelo:")
        self.r2_label = QLabel("R²: ")
        self.mse_label = QLabel("ECM: ")
        self.intercept_label = QLabel("Intercepto: ")
        self.coefficients_label = QLabel("Coeficiente: ")
        self.input_columns_label = QLabel("Columnas de entrada:")
        self.output_column_label = QLabel("Columnas de salida:")
        
        # Add widgets to the layout
        model_info_layout.addWidget(self.formula_label)
        model_info_layout.addWidget(self.r2_label)
        model_info_layout.addWidget(self.mse_label)
        model_info_layout.addWidget(self.intercept_label)
        model_info_layout.addWidget(self.coefficients_label)
        model_info_layout.addWidget(self.input_columns_label)
        model_info_layout.addWidget(self.output_column_label)

        # Add model description functionality
        self.model_description.add_to_layout(model_info_layout)
        model_info_group.setLayout(model_info_layout)

        # Group 3: Prediction and visualization
        # Prediction group
        prediction_group = QGroupBox("Predicción")
        prediction_layout = QVBoxLayout()
        prediction_layout.setSpacing(0)
        prediction_layout.setContentsMargins(10, 5, 10, 10)

        # Create a scroll area for the input container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Container for prediction inputs
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout(self.input_container)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setSpacing(0)
        self.input_container.setStyleSheet("background: transparent;")
        scroll_area.setWidget(self.input_container)
        prediction_layout.addWidget(scroll_area)
        
        # Prediction label (hidden initially)
        self.prediction_label = QLabel()
        self.prediction_label.setObjectName("prediction_label")
        self.prediction_label.setVisible(False)
        prediction_layout.addWidget(self.prediction_label)
        prediction_layout.setSpacing(30)
        
        # Prediction button
        self.predict_button = QPushButton("Realizar Predicción")
        self.predict_button.setFixedHeight(50)
        self.predict_button.setVisible(False)
        self.predict_button.clicked.connect(self.make_prediction)
        prediction_layout.addWidget(self.predict_button)
        prediction_group.setLayout(prediction_layout)

        # Add prediction group to left container
        left_widget = QWidget()
        left_widget.setLayout(left_container)
        left_widget.setFixedWidth(600)
        
        left_container.addWidget(model_info_group)
        left_container.addWidget(prediction_group)

        # Save button below the prediction group
        self.save_button = QPushButton("💾 Guardar Modelo")
        self.save_button.setFixedHeight(50)
        self.save_button.clicked.connect(self.save_model)
        self.save_button.setVisible(False)
        left_container.addWidget(self.save_button)
        # Visualization group (right)
        visualization_group = QGroupBox("Visualización")
        visualization_layout = QVBoxLayout()
        visualization_layout.setContentsMargins(10, 10, 10, 10)
        
        # Graph container
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        visualization_layout.addWidget(self.graph_container)

        # Set size policy for visualization group
        visualization_group.setLayout(visualization_layout)
        visualization_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add both sides to content layout
        content_layout.addWidget(left_widget)
        content_layout.addWidget(visualization_group, 1)

        # Add content layout to the main layout
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def setup_model_display(self, model_data: dict):
        """
        Displays the information of a model (new or loaded) on the UI.

        Parameters
        ----------
        model_data : dict
            A dictionary containing model details like formula, metrics, description, and columns.
        """
        try:
            # Update UI labels with model formula and metrics
            self.formula_label.setText(f"Fórmula del Modelo: {model_data['formula']}")
            self.r2_label.setText(f"R²: {float(model_data['metrics']['r2_score']):.4f}")
            self.mse_label.setText(f"ECM: {float(model_data['metrics']['rmse']):.4f}")
            
            # Update the model description if provided
            if 'description' in model_data:
                self.model_description.set_description(model_data['description'])

            # Enable word wrap on labels that can have long text
            self.formula_label.setWordWrap(True)
            self.coefficients_label.setWordWrap(True)
            self.input_columns_label.setWordWrap(True)
            
            # Show intercept and coefficients
            intercept = model_data['intercept']
            coefficients = model_data['coefficients']
            if intercept is not None:
                self.intercept_label.setText(f"Intercepto: {intercept:.4f}")
                self.intercept_label.setVisible(True)
            if coefficients is not None:
                coefficients_text = ", ".join(f"{coef:.4f}" for coef in coefficients)
                self.coefficients_label.setText(f"Coeficientes: [{coefficients_text}]")
                self.coefficients_label.setVisible(True)

            # Show input and output columns
            self.input_columns = model_data['columns']['input']
            self.output_column = model_data['columns']['output']
            self.input_columns_label.setText(f"Columnas de Entrada: {', '.join(self.input_columns)}")
            self.input_columns_label.setVisible(True)
            self.output_column_label.setText(f"Columna de Salida: {self.output_column}")
            self.output_column_label.setVisible(True)
            
            # Configure input fields for prediction
            self.input_columns = model_data['columns']['input']
            self.output_column = model_data['columns']['output']
            self.create_prediction_inputs()
            
            # Show prediction and save buttons
            self.predict_button.setVisible(True)
            self.save_button.setVisible(True)
            self.enable_line_edits()

            # Refresh the UI after updates
            self.update()
            QApplication.processEvents()

        except Exception as e:
            show_error(f"Error al mostrar datos del modelo: {str(e)}", self)
            raise

    def initialize_from_loaded_model(self, loaded_model: dict):
        """Initializes the tab with details from a pre-loaded model."""
        try:
            # Reconstruct the model using its coefficients and intercept
            self.model = LinearModel(None, 
                                loaded_model['columns']['input'],
                                loaded_model['columns']['output'])
            self.model.coef_ = np.array(loaded_model['coefficients'])
            self.model.intercept_ = float(loaded_model['intercept'])
            self.model.formula = loaded_model['formula']
            
            # Display the loaded model's details on the UI
            self.setup_model_display({
                'formula': loaded_model['formula'],
                'metrics': loaded_model['metrics'],
                'description': loaded_model['description'],
                'columns': loaded_model['columns'],
                'intercept': loaded_model['intercept'],
                'coefficients': loaded_model['coefficients']
                })
            
        except Exception as e:
            show_error(f"Error al inicializar el modelo cargado: {str(e)}", self)
            raise

    def initialize_for_new_model(self):
        """
        Prepares the tab for a new model, enabling prediction input fields.
        """
        self.create_prediction_inputs()

    def create_prediction_inputs(self):
        """
        Dynamically creates input fields for prediction based on input columns.
        """
        for widget in self.input_widgets:
            widget[0].setParent(None)
            widget[1].setParent(None)
        self.input_widgets.clear()
        
        if self.input_columns:
            # Dynamically create label and input field pairs for each input column
            for column in self.input_columns:
                container = QWidget()
                container_layout = QVBoxLayout(container)
                container_layout.setContentsMargins(0, 0, 0, 0)
                container_layout.setSpacing(0)
                
                # Label for the input column
                label = QLabel(f"{column}:")
                label.setFixedHeight(25)
                
                # Input field for the column
                line_edit = QLineEdit()
                line_edit.setFixedHeight(30)
                line_edit.setFixedWidth(230)
                
                # Add label and input field to the container
                container_layout.addWidget(label)
                container_layout.addWidget(line_edit)
                
                # Track the label and input field for later use
                self.input_widgets.append((label, line_edit))
                self.input_layout.addWidget(container)
                
                # Set visibility based on whether a model is loaded
                label.setVisible(self.model is not None)
                line_edit.setVisible(self.model is not None)
                
            # Add spacing at the end of the inputs
            self.input_layout.addStretch()

    def create_model(self):
        """
        Creates a new linear regression model using the provided data and columns.
        """
        # Clear any existing graphs
        self.clear_previous_graph()
        try:
            # Check for null values in the selected columns
            selected_columns = self.input_columns + [self.output_column]
            if self.data[selected_columns].isnull().any().any():
                show_error("⚠ Error al crear el modelo lineal: Debe preprocesar los datos en la pestaña de datos antes de seguir ⚠", self)
                return
            
            # Initialize and fit the model
            self.model = LinearModel(self.data, self.input_columns, self.output_column)
            self.model.fit()

            # Display the model's details on the UI
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
                },
                'intercept': self.model.intercept_,
                'coefficients': self.model.coef_
            })

            # Create a visualization based on the number of input columns
            if len(self.model.input_columns) == 1:
                self.plot2d_graph()
                self.toolbar = NavigationToolbar2QT(self.canvas, self)
                self.graph_layout.addWidget(self.toolbar)
            elif len(self.model.input_columns) == 2:
                self.plot3d_graph()
                self.toolbar = NavigationToolbar2QT(self.canvas, self)
                self.graph_layout.addWidget(self.toolbar)
            else:
                res = "No se puede crear una gráfica con más de 2 columnas de entrada. "
                res += "Para visualizar el modelo, seleccione un máximo de 2 variables independientes."
                show_message(res, self)

            show_message("El modelo de regresión lineal ha sido creado exitosamente.", self)

        except Exception as e:
            show_error(f"Error al crear el modelo lineal: {str(e)}", self)

    def enable_line_edits(self) -> None:
        # Show all associated QLabel and QLineEdit
        for label, line_edit in self.input_widgets:
            label.setVisible(True)
            line_edit.setVisible(True)

    def clear_previous_graph(self):
        """
        Removes any existing graph from the UI.
        """
        if self.canvas:
            self.canvas.setParent(None)
            self.canvas.deleteLater()
            self.canvas = None
            self.graph_layout.removeWidget(self.toolbar)
            
    def plot2d_graph(self):
        """
        Creates and displays a 2D graph for models with one input column.
        """
        if not hasattr(self.model, 'x') or not hasattr(self.model, 'y'):
            return      
        # Create the figure and canvas for the graph
        fig = Figure(figsize=(4, 3), dpi=50)
        self.canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot(111)
        ax.set_facecolor('none')

        # Plot the real data and regression line
        ax.scatter(self.model.x, self.model.y, label="Datos Reales")
        ax.plot(self.model.x, self.model.y_pred, color='red', label="Línea de Regresión")
        ax.set_xlabel(self.model.input_columns[0])
        ax.set_ylabel(self.model.output_column)
        ax.legend()

        # Add the canvas to the graph layout
        self.graph_layout.addWidget(self.canvas)
        self.canvas.draw()

    def plot3d_graph(self):
        """
        Creates and displays a 3D graph for models with two input columns.
        """
        fig = Figure(figsize=(4, 3), dpi=75)
        self.canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot(111, projection = "3d")
        ax.set_facecolor('none')

        # Extract variables for the graph
        var1 = [x[0] for x in self.model.x]
        var2 = [x[1] for x in self.model.x]
        min1 , max1 = self.minmax(var1)
        min2, max2 = self.minmax(var2)
        
        # Plot real data points
        ax.plot(var1, var2, self.model.y, 'o', markersize = 2, alpha = 0.5, label = "Datos Reales")
        
        # Generate a regression plane
        x, y = np.meshgrid(np.linspace(min1,  max1, 20), np.linspace(min2, max2, 20))
        z = self.model.intercept_ + self.model.coef_[0] * x + self.model.coef_[1] * y
        ax.plot_surface(x, y, z, color = "red", alpha = 0.5, label = "Plano de Regresion")
        ax.legend()
        
        # Add the canvas to the graph layout
        self.graph_layout.addWidget(self.canvas)
        self.canvas.draw()

    def minmax(self, v:list[float]) -> tuple[int]:
        """
        Computes the minimum and maximum values of a list.

        Parameters
        ----------
        v : list[float]
            List of numerical values.

        Returns
        -------
        tuple[float, float]
            The minimum and maximum values of the list.
        """
        mn = v[0]
        mx = v[0]
        for x in v[1:]:
            if x < mn:
                mn = x
            if x > mx:
                mx = x
        return (mn, mx)

    def save_model(self):
        """
        Saves the trained linear regression model to a file.
        The model data includes the formula, coefficients, intercept, description, 
        metrics (R², RMSE), and column information.
        """
        if not self.model:
            show_error('⚠ Debe primero entrenar o cargar un modelo ⚠')
            return

        # Check if model has description and show recommendation dialog if not
        description = self.model_description.get_description()
        if not description:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Recomendación")
            msg_box.setText("El modelo no tiene una descripción.")
            msg_box.setInformativeText("Se recomienda añadir una descripción para mejor documentación. ¿Desea continuar sin descripción?")
            
            # Create custom button
            si_button = msg_box.addButton("Sí", QMessageBox.YesRole)
            no_button = msg_box.addButton("No", QMessageBox.NoRole)
            msg_box.setDefaultButton(no_button)
            
            msg_box.exec_()
            if msg_box.clickedButton() == no_button:
                return
        
        try:
            # Use existing metrics for loaded models, or compute metrics for new ones
            if hasattr(self, 'loaded_model') and self.loaded_model is not None:
                metrics = self.loaded_model['metrics']
            else:
                metrics = {
                    'r2_score': float(self.model.r2_) if hasattr(self.model, 'r2_') 
                            else r2_score(self.model.y, self.model.y_pred),
                    'rmse': float(self.model.mse_) if hasattr(self.model, 'mse_') 
                        else mean_squared_error(self.model.y, self.model.y_pred)
                }

            # Prepare the model data dictionary
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
        
            # Save model dialog
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

        # Refresh the UI
        self.layout().update()

        # Retrieve user-entered values from input fields
        input_values = []
        for label, line_edit in self.input_widgets:
            value = line_edit.text()
            if not value:
                show_warning("Debe rellenar todas las celdas para realizar predicción.", self)
                return None
                
            try:
                input_values.append(float(value))
            except ValueError:
                show_error(f"Todos los valores deben ser numéricos.", self)
                return None

        try:
            # Compute the prediction using the model's coefficients and intercept
            prediction = self.model.intercept_
            for i in range(len(input_values)):
                prediction += self.model.coef_[i] * input_values[i]
        

            # Display the prediction result
            self.prediction_label.setText(f"Resultado de la predicción:\n{self.output_column} = {prediction:.4f}")
            self.prediction_label.setVisible(True)  # Mostrar el QLabel

        except ValueError:
            show_error("Por favor, introduzca solo valores numéricos.", self)