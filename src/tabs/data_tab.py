from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from typing import List, Optional
import joblib
from os.path import splitext
from data_processing.import_module import DataFrame, load_file
from ui.popup_handler import (InputDialog, open_file_dialog,
    open_model_dialog, show_error, show_message, QtCore)
from data_processing.dataset_calc import PreprocessApplier, none_count
from ui.components.column_selector import ColumnSelector
from ui.components.data_table import DataTable
from ui.components.preprocess_toolbar import PreprocessToolbar

class DataTab(QWidget):
    """
    Data tab that manages data loading, selection, and preprocessing.

    This class organizes the GUI elements related to file loading, column selection,
    and preprocessing options, facilitating user interaction and operations on a DataFrame.

    Attributes
    ----------
    data : DataFrame, optional
        The DataFrame containing the loaded data.
    selected_input_columns : List[str], optional
        List of columns selected as inputs for analysis.
    preprocess_applier : PreprocessApplier
        Object for managing and applying the selected preprocessing method.
    load_button : QPushButton
        Button to open a data file.
    file_path_label : QLabel
        Label displaying the loaded file path.
    table : DataTable
        Table showing a preview of the loaded data.
    column_selector : ColumnSelector
        Column selector to choose input and output columns.
    preprocess_label : QLabel
        Label describing the preprocessing options.
    preprocess_toolbar : PreprocessToolbar
        Toolbar with buttons for preprocessing options.

    """


    def __init__(self):
        """
        Initializes the DataTab class and sets up the user interface components.
        """
        super().__init__()
        self.data: Optional[DataFrame] = None
        self.selected_input_columns: Optional[List[str]] = None
        self.selected_output_column: Optional[str] = None
        self.preprocess_applier = PreprocessApplier()
        self.init_ui()

    def init_ui(self):
        """
        Initializes the data tab's user interface, including buttons, labels,
        and tables for data loading and preprocessing selection.
        """
        layout = QVBoxLayout()

        # Section for loading files
        self.load_widget = QWidget()
        load_bar = QHBoxLayout(self.load_widget)
        
        # File and model loading buttons
        self.file_button = QPushButton('📂 Abrir Archivo')
        self.file_button.setFixedSize(200, 50)
        self.model_button = QPushButton('🗃️ Cargar Modelo')
        self.model_button.setFixedSize(200, 50)
        self.path_label = QLabel('Ruta del archivo cargado:')

        # Data preview table
        self.table = DataTable()

        # Initialize column selector and preprocessing section
        self.init_selector()
        self.init_preprocess()
        
        # Connect buttons to their respective actions
        self.connect_buttons()
        
        # Add widgets to the loading bar layout
        load_bar.addWidget(self.file_button)
        load_bar.addWidget(self.model_button)
        load_bar.addWidget(self.path_label)
        
        # Add components to the main layout
        layout.addWidget(self.load_widget)
        layout.addWidget(self.table)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.preprocess_label)
        layout.addWidget(self.preprocess_toolbar)

        self.setLayout(layout)

    def init_selector(self):
        """
        Initializes the column selector component and connects its signals.
        """
        # The column selector is initially hidden
        self.column_selector = ColumnSelector()
        self.column_selector.setVisible(False)

        # Connect signals for column selection changes and confirmation
        self.column_selector.confirm_button.clicked.connect(
            self.on_selection_confirmed)
        self.column_selector.input_column_selector.itemChanged.connect(
            self.on_input_column_selection_changed)
        self.column_selector.output_column_selector.textActivated.connect(
            self.on_output_column_selection_changed)

    def init_preprocess(self):
        # Sección de preprocesado
        self.preprocess_label = QLabel(
            'Seleccione una opción de preprocesado de datos nulos:')
        self.preprocess_label.hide()
        self.preprocess_toolbar = PreprocessToolbar()

    def connect_buttons(self):
        # Connect file loading button
        self.file_button.clicked.connect(self.load_data)
        
        # Connect preprocessing toolbar buttons
        self.preprocess_toolbar.buttons['delete'].clicked.connect(
            lambda: self.set_preprocessing_method('delete'))
        self.preprocess_toolbar.buttons['mean'].clicked.connect(
            lambda: self.set_preprocessing_method('mean'))
        self.preprocess_toolbar.buttons['median'].clicked.connect(
            lambda: self.set_preprocessing_method('median'))
        self.preprocess_toolbar.buttons['constant'].clicked.connect(
            self.handle_constant_method)
        # Connect apply button to trigger preprocessing and model creation if successful
        self.preprocess_toolbar.apply_button.clicked.connect(
            lambda: (
                self.apply_preprocessing() and 
                self.column_selector.confirm_button.clicked.emit()
            )
        )

    def load_model(self):
        """    
        Loads a model and returns it if successful.
        """
        model_path = open_model_dialog(self)

        # Displays an error if the loaded file's extension is not '.joblib'
        if splitext(model_path)[1] != '.joblib':
            show_error('⚠ Error al cargar el modelo: Formato de archivo no válido ⚠', self)
            return None

        try:
            # Load the model from the file
            model_data = joblib.load(model_path)

            # Ensure the model has the required keys
            required_keys = ['formula', 'coefficients', 'intercept', 'metrics', 'columns']
            if not all(key in model_data for key in required_keys):
                show_error("⚠ El archivo no contiene un modelo válido ⚠", self)
                return None
            
            # Hide table and column selector for clarity
            self.column_selector.setVisible(False)
            self.preprocess_label.hide()
            self.preprocess_toolbar.hide_buttons()
            
            # Display the loaded file path and confirmation message
            self.path_label.setText(
                f'📄 Ruta del modelo cargado: {model_path}')
            show_message('✅ ¡Modelo cargado exitosamente! 😃', self)
            
            return model_data
        except Exception as e:
            show_error(f'⚠ Error al cargar el modelo: {str(e)} ⚠', self)
            return None
    
    def load_data(self):
        """
        Loads a data file selected by the user, updating the table and column selector.

        Notes
        -----
        Uses `im.load_file` to load the file and `show_message` to notify the user
        in case of success or failure.
        """
        file_path = open_file_dialog(self)
        if not file_path:
            return

        try:
            # Load the dataset into the table and initialize column selection
            self.data = load_file(file_path)
            self.path_label.setText(
                f'📄 Ruta del archivo cargado: {file_path}')
            self.table.load_data(self.data, batch_size=100)
            self.column_selector.populate_columns(self.data)
            self.column_selector.setVisible(True)
            show_message('✅ ¡Archivo cargado exitosamente! 😃', self)
                
        except Exception as e:
            show_error(f'⚠ {str(e)} ⚠', self)

    def on_input_column_selection_changed(self, item):
        """
        Highlights a column in the table when it is selected or deselected
        in the column selector.

        Parameters
        ----------
        item : QListWidgetItem
            List item in `input_column_selector` that has changed state.
        """
        # Get the index of the column and its selection state
        column_index = self.column_selector.input_column_selector.row(item)
        state = item.checkState()

        # Highlight the selected column in the table
        if column_index !=\
            self.column_selector.output_column_selector.currentIndex() or state:
            self.table.highlight_column(column_index, state)
        
    def on_output_column_selection_changed(self):
        """
        Highlights a column in the table when it is selected or deselected
        in the column selector.

        Parameters
        ----------
        item : QListWidgetItem
            List item in `input_column_selector` that has changed state.
        """
        # Get the current and previously selected output column indices
        current_column_index = self.column_selector.output_column_selector.currentIndex()
        last_column_index = self.column_selector.output_column_selector.last_selected
        
        # Highlight the current output column
        self.table.highlight_column(current_column_index, True)

        # Unhighlight the last column if it is no longer selected
        if not self.column_selector.input_column_selector.item(
            last_column_index).checkState() and\
                last_column_index != current_column_index:

            self.table.highlight_column(
                last_column_index, False)

    def on_selection_confirmed(self):
        """
        Confirms the columns selected by the user and enables the preprocessing interface.

        Raises
        ------
        ValueError
            If no input columns or an output column are selected.
        """
        # Retrieve the selected input and output columns
        input_columns, output_column = self.column_selector.get_selected_columns()

        if not input_columns:
            return
        elif output_column == "":
            return

        # Store the selected columns and display a summary
        self.selected_input_columns = input_columns
        self.selected_output_column = output_column
        self.none_columns = none_count(self.data, input_columns + [output_column])
        self.show_selection_summary(input_columns, output_column)
        
        # Enable preprocessing if there are null values
        if sum(map(int, none_count(self.data, input_columns + [output_column]))) > 0:
            self.enable_preprocessing()
        else:
            self.disable_preprocessing()

    def set_preprocessing_method(self, method: str):
        """
        Sets the current preprocessing method and displays the 'Apply' button.

        Parameters
        ----------
        method : str
            Preprocessing method to apply ('delete', 'mean', 'median', 'constant').
        """
        self.preprocess_applier.set_current_method(method)

    def show_selection_summary(self, input_columns: List[str], output_column: str):
        """
        Displays a summary of the selected columns in a pop-up message.

        Parameters
        ----------
        input_columns : List[str]
            List of column names selected as input.
        output_column : str
            Name of the column selected as output.
        """
        summary = (
            f'Columnas de entrada: {", ".join(input_columns)}\n'
            f'Valores nulos: {", ".join(map(str, none_count(self.data, input_columns + [output_column])))}\n'
            f'Columna de salida: {output_column}'
        )
        show_message(summary, self)

    def enable_preprocessing(self):
        """
        Shows the preprocessing section in the interface, allowing the user
        to select and apply a preprocessing method.
        """
        self.preprocess_label.show()
        self.preprocess_toolbar.show_buttons()

    def disable_preprocessing(self):
        """
        Hides the preprocessing section in the interface, not allowing the user
        to select and apply a preprocessing method.
        """
        self.preprocess_label.hide()
        self.preprocess_toolbar.hide_buttons()

    def handle_constant_method(self):
        """
        Shows an input dialog to define constant values by column
        when the user selects the constant preprocessing method.

        Notes
        -----
        This method only activates if input columns are selected.
        """
        if self.selected_input_columns:

            # Combine selected input columns and output column
            selected_columns = self.selected_input_columns + [self.selected_output_column]

            # Filter columns that are selected and contain null values
            null_columns = [
                column for column in selected_columns
                if column in self.data.columns and self.data[column].isnull().any()]
            
            # Create and display the input dialog for constants
            input_window = InputDialog(
                null_columns, 'Introduzca las constantes', parent = self)
            input_window.exec()

            # Retrieve the constants entered by the user
            constants = input_window.get_inputs()
            self.preprocess_applier.set_current_method('constant', constants)

    def apply_preprocessing(self):
        """
        Applies the selected preprocessing method to the loaded data
        and updates the table and column selector.

        Raises
        ------
        Exception
            If an error occurs during data preprocessing.

        Returns
        -------
        bool
            True if preprocessing was successful, False otherwise
        """
        try:
            # Apply the preprocessing method to the selected columns
            self.preprocess_applier.apply_preprocess(
                self.data,
                self.selected_input_columns + [self.selected_output_column])

            # Update the data table with the preprocessed data
            self.table.load_more_rows()

            self.on_output_column_selection_changed()

            show_message('✅ ¡Preprocesado aplicado exitosamente!', self)
            return True
        except Exception as e:
            show_error(f'Error al aplicar el preprocesado: {str(e)}', self)
            return False
