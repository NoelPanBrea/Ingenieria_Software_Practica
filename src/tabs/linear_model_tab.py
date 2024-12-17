import joblib
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, 
    QHBoxLayout, QApplication, QGroupBox, QScrollArea, QFrame)
from models.linear_model import LinearModel
from models.plot_manager import PlotManager
from ui.components.groups import CreationGroup, InfoGroup, PredictionGroup, Qt
from sklearn.metrics import mean_squared_error, r2_score
from ui.popup_handler import (show_error, show_message, 
    show_warning, show_suggestion, save_file_dialog)



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
        self.data = data
        self.input_columns = input_columns
        self.output_column = output_column
        self.model = None
        self.loaded_model = loaded_model
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

            model_creation_group = CreationGroup()
            model_creation_group.button.clicked.connect(self.create_model)
            main_layout.addWidget(model_creation_group)

        # Create horizontal layout for main content
        content_layout = QHBoxLayout()
        
        # Left side container with vertical layout
        left_container = QVBoxLayout()
        
        # Group 2: Model information
        self.model_info_group = InfoGroup()
        self.model_description = self.model_info_group.model_description

        # Group 3: Prediction and visualization
        # Prediction group
        self.prediction_group = PredictionGroup()
       
        # Prediction button
        self.prediction_group.button.clicked.connect(self.make_prediction)

        # Add prediction group to left container
        left_widget = QWidget()
        left_widget.setLayout(left_container)
        left_widget.setFixedWidth(600)
        
        left_container.addWidget(self.model_info_group)
        left_container.addWidget(self.prediction_group)

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
        self.plot_manager = PlotManager(self.graph_layout)
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
            self.model_info_group.set_label_texts(model_data)
            self.input_columns = model_data["columns"]["input"]
            self.output_column = model_data["columns"]["output"]
            self.prediction_group.create_prediction_inputs(self.input_columns, self.model is not None)
            # Show prediction and save buttons
            self.prediction_group.enable_line_edits()
            self.prediction_group.button.setVisible(True)
            self.save_button.setVisible(True)
   
            

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
                                loaded_model["columns"]["input"],
                                loaded_model["columns"]["output"])
            self.model.coef_ = np.array(loaded_model["coefficients"])
            self.model.intercept_ = float(loaded_model["intercept"])
            self.model.formula = loaded_model["formula"]
            
            # Display the loaded model's details on the UI
            self.setup_model_display({
                "formula": loaded_model["formula"],
                "metrics": loaded_model["metrics"],
                "description": loaded_model["description"],
                "columns": loaded_model["columns"],
                "intercept": loaded_model["intercept"],
                "coefficients": loaded_model["coefficients"]
                })

        except Exception as e:
            show_error(f"Error al inicializar el modelo cargado: {str(e)}", self)
            raise

    def initialize_for_new_model(self):
        """
        Prepares the tab for a new model, enabling prediction input fields.
        """
        self.prediction_group.create_prediction_inputs(self.input_columns, self.model is not None)


    def create_model(self):
        """
        Creates a new linear regression model using the provided data and columns.
        """
        # Clear any existing graphs
        self.plot_manager.clear()
        try:
            # Check for null values in the selected columns
            selected_columns = self.input_columns + [self.output_column]
            
            # Initialize and fit the model
            self.model = LinearModel(self.data, self.input_columns, self.output_column)
            self.model.fit()

            # Display the model's details on the UI
            self.setup_model_display({
                "formula": self.model.formula,
                "metrics": {
                    "r2_score": self.model.r2_,
                    "rmse": self.model.mse_
                },
                "description": self.model_description.get_description(),
                "columns": {
                    "input": self.input_columns,
                    "output": self.output_column
                },
                "intercept": self.model.intercept_,
                "coefficients": self.model.coef_
            })

            # Create a visualization based on the number of input columns
            if len(self.model.input_columns) == 1:
                self.plot_manager.plot2d(self.model.x, self.model.y,
                        self.model.y_pred, selected_columns)
                self.plot_manager.draw()
            elif len(self.model.input_columns) == 2:
                x = [x[0] for x in self.model.x]
                z = [x[1] for x in self.model.x]
                x = np.linspace(min(x), max(x), 20)
                z = np.linspace(min(z), max(z), 20)
                prediction = np.linspace(min(self.model.y_pred), max(self.model.y_pred), 20)
                x, z, prediction = np.meshgrid(x, z, prediction)
                self.plot_manager.plot3d(x, z, self.model.y,
                    prediction, selected_columns)
                self.plot_manager.draw()
            else:
                res = "No se puede crear una gráfica con más de 2 columnas de entrada. "
                res += "Para visualizar el modelo, seleccione un máximo de 2 variables independientes."
                show_message(res, self)
            
            show_message("El modelo de regresión lineal ha sido creado exitosamente.", self)

        except Exception as e:
            show_error(f"Error al crear el modelo lineal: {str(e)}", self)

    def save_model(self):
        """
        Saves the trained linear regression model to a file.
        The model data includes the formula, coefficients, intercept, description, 
        metrics (R², RMSE), and column information.
        """
        if not self.model:
            show_error("⚠ Debe primero entrenar o cargar un modelo ⚠")
            return

        # Check if model has description and show recommendation dialog if not
        description = self.model_description.get_description()
        if not description:
            show_suggestion()
        try:
            # Use existing metrics for loaded models, or compute metrics for new ones
            if hasattr(self, "loaded_model") and self.loaded_model is not None:
                metrics = self.loaded_model["metrics"]
            else:
                metrics = {
                    "r2_score": float(self.model.r2_) if hasattr(self.model, "r2_") 
                            else r2_score(self.model.y, self.model.y_pred),
                    "rmse": float(self.model.mse_) if hasattr(self.model, "mse_") 
                        else mean_squared_error(self.model.y, self.model.y_pred)
                }

            # Prepare the model data dictionary
            model_data = {
                "formula": self.model.formula,
                "coefficients": self.model.coef_.tolist(),
                "intercept": float(self.model.intercept_),
                "description": self.model_description.get_description(),
                "metrics": metrics,
                "columns": {
                    "input": self.input_columns,
                    "output": self.output_column
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
        for label, line_edit in self.prediction_group.input_widgets:
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
            prediction = self.model.predict(input_values)

            # Display the prediction result
            self.prediction_group.label.setText(f"Resultado de la predicción:\n{self.output_column} = {prediction:.4f}")
            self.prediction_group.label.setVisible(True)  # Mostrar el QLabel

        except ValueError:
            show_error("Por favor, introduzca solo valores numéricos.", self)