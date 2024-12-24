from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QFrame, QLabel, QWidget, QLineEdit
from models.description import ModelDescription, Qt


class BasicGroup(QGroupBox):
    """
    Base class for Groups.

    Attributes
    ----------

    """

    def __init__(self, name: str):
        super().__init__(name)


class CreationGroup(BasicGroup):
    """
    Subclass of Basic Group that handles the 
    display of the creation group in the app.

    Attributes
    ----------
    layout : QLayout
       Main layout of the group.
    button : QPushButton
        Main button of the layout.
    """

    def __init__(self):
        """
        Initialices the whole class.
        """

        super().__init__("Creación del modelo")
        self.setFixedHeight(100)
        self._button = QPushButton("Crear Modelo de Regresión Lineal")
        self.init_ui()

    def init_ui(self):
        self._layout = QHBoxLayout()
        self._button.setFixedSize(350, 50)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._button, Qt.AlignCenter)
        self.setLayout(self._layout)

    @property
    def layout(self):
        return self._layout

    @property
    def button(self) -> QPushButton:
        return self._button


class InfoGroup(BasicGroup):
    """
    Subclass of Basic Group that handles the 
    display of the creation group in the app.

    Attributes
    ----------
    model_description : ModelDescription
       Model description widget of the group.
    container : QWidget
        container for the scroll_area.
    scroll_area : QScrollArea
        Scroll area for the label widgets.
    *_label : QLabel
        multiple labels for the scroll area.
    layout : QLayout
       Inner layout of the group.
    outer_layout : QLayout
        Outer layout of the group.
    """

    def __init__(self):
        """
        Initialices the whole class.
        """

        super().__init__("Información del Modelo")
        self._model_description = ModelDescription(self)
        self.container = QWidget()
        self.scroll_area = QScrollArea()
        self.formula_label = QLabel("Fórmula del Modelo:")
        self.r2_label = QLabel("R²: ")
        self.mse_label = QLabel("ECM: ")
        self.intercept_label = QLabel("Intercepto: ")
        self.coefficients_label = QLabel("Coeficiente: ")
        self.input_columns_label = QLabel("Columnas de entrada:")
        self.output_column_label = QLabel("Columnas de salida:")
        self.init_ui()

    def init_ui(self):
        self.outer_layout = QVBoxLayout()
        self.outer_layout.setContentsMargins(10, 10, 10, 10)
        self.outer_layout.setSpacing(5)
        self._layout = QVBoxLayout(self.container)
        self._layout.setContentsMargins(10, 10, 10, 10)
        self._layout.setSpacing(5)
        # Config the scroll area
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setWidget(self.container)
        # Add widgets to the layouts
        self._layout.addWidget(self.formula_label)
        self._layout.addWidget(self.r2_label)
        self._layout.addWidget(self.mse_label)
        self._layout.addWidget(self.intercept_label)
        self._layout.addWidget(self.coefficients_label)
        self._layout.addWidget(self.input_columns_label)
        self._layout.addWidget(self.output_column_label)
        self.outer_layout.addWidget(self.scroll_area)
        self._model_description.add_to_layout(self.outer_layout)
        self.setLayout(self.outer_layout)

    @property
    def model_description(self):
        return self._model_description

    @property
    def layout(self):
        return self._layout

    def set_label_texts(self, model_data: dict):
        """
        Gives the label widgets text to show.
        """

        # Update UI labels with model formula and metrics
        self.formula_label.setText(f"Fórmula del Modelo: {\
                                   model_data['formula']}")
        self.r2_label.setText(
            f"R²: {float(model_data['metrics']['r2_score']):.4f}")
        self.mse_label.setText(
            f"ECM: {float(model_data['metrics']['rmse']):.4f}")

        # Update the model description if provided
        if "description" in model_data:
            self._model_description.set_description(model_data["description"])

        # Enable word wrap on labels that can have long text
        self.formula_label.setWordWrap(True)
        self.coefficients_label.setWordWrap(True)
        self.input_columns_label.setWordWrap(True)

        # Show intercept and coefficients
        intercept = model_data["intercept"]
        coefficients = model_data["coefficients"]
        if intercept is not None:
            self.intercept_label.setText(f"Intercepto: {intercept:.4f}")
            self.intercept_label.setVisible(True)
        if coefficients is not None:
            coefficients_text = ", ".join(
                f"{coef:.4f}" for coef in coefficients)
            self.coefficients_label.setText(
                f"Coeficientes: [{coefficients_text}]")
            self.coefficients_label.setVisible(True)

            # Show input and output columns
            self.input_columns = model_data["columns"]["input"]
            self.output_column = model_data["columns"]["output"]
            self.input_columns_label.setText(
                f"Columnas de Entrada: {', '.join(self.input_columns)}")
            self.input_columns_label.setVisible(True)
            self.output_column_label.setText(
                f"Columna de Salida: {self.output_column}")
            self.output_column_label.setVisible(True)

            # Configure input fields for prediction
            self.input_columns = model_data["columns"]["input"]
            self.output_column = model_data["columns"]["output"]


class PredictionGroup(BasicGroup):
    """
    Subclass of Basic Group that handles the 
    display of the creation group in the app.

    Attributes
    ----------
    model_description : ModelDescription
       Model description widget of the group.
    container : QWidget
        container for the scroll_area.
    scroll_area : QScrollArea
        Scroll area for the label widgets.
    *_label : QLabel
        multiple labels for the scroll area.
    layout : QLayout
       Inner layout of the group.
    outer_layout : QLayout
        Outer layout of the group.
    button : QLayout
        main button of the group.
    """

    def __init__(self):
        """
        Initialices the whole class.
        """

        super().__init__("Predicción")
        self.container = QWidget()
        self._button = QPushButton("Realizar Predicción")
        self._label = QLabel()
        self.scroll_area = QScrollArea()
        self.input_widgets = []
        self.init_ui()

    def init_ui(self):
        self.outer_layout = QVBoxLayout()
        self.outer_layout.setSpacing(0)
        self.outer_layout.setContentsMargins(10, 5, 10, 10)
        self._layout = QVBoxLayout(self.container)
        self._button.setFixedHeight(50)
        self._button.setVisible(False)
        self._label.setVisible(False)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.scroll_area.setMinimumHeight(200)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setWidget(self.container)

        self.outer_layout.addWidget(self.scroll_area)
        self.outer_layout.addWidget(self._label)
        self.outer_layout.setSpacing(30)
        self.outer_layout.addWidget(self._button, Qt.AlignBottom)
        self.setLayout(self.outer_layout)

    @property
    def layout(self):
        return self._layout

    @property
    def label(self):
        return self._label

    @property
    def button(self) -> QPushButton:
        return self._button

    def enable_line_edits(self):
        # Show all associated QLabel and QLineEdit
        for label, line_edit in self.input_widgets:
            label.setVisible(True)
            line_edit.setVisible(True)

    def create_prediction_inputs(self, input_columns: list, modelmade: bool):
        """
        Dynamically creates input fields for prediction based on input columns.
        """
        # Dynamically create label and input field pairs for each input column
        for widget in self.input_widgets:
            widget[0].setParent(None)
            widget[1].setParent(None)
        self.input_widgets.clear()

        if input_columns:

            for column in input_columns:

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
                self._layout.addWidget(container)
                line_edit.setVisible(modelmade)
                label.setVisible(modelmade)

            # Add spacing at the end of the inputs
            self.outer_layout.addStretch()
