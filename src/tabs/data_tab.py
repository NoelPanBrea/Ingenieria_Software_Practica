from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt
from typing import List, Optional
import pandas as pd
import joblib
import numpy as np

import tabs.data_aux.import_module as im
from tabs.data_aux.common_aux.popup_handler import *
from tabs.data_aux.dataset_calc import *
from tabs.data_aux.column_selector import ColumnSelector
from tabs.data_aux.data_table import DataTable
from tabs.data_aux.preprocess_toolbar import PreprocessToolbar
from tabs.lineal_model_tab import LinealModelTab
from tabs.lineal_model_aux.class_LinealModel import LinealModel

class DataTab(QWidget):
    """
    Data tab that manages data loading, selection, and preprocessing.

    This class organizes the GUI elements related to file loading, column selection,
    and preprocessing options, facilitating user interaction and operations on a DataFrame.

    Attributes
    ----------
    data : pd.DataFrame, optional
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
        super().__init__()
        self.data: Optional[pd.DataFrame] = None
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

        # Sección de carga de archivo
        self.load_widget = QWidget()
        load_bar = QHBoxLayout(self.load_widget)
        
        self.file_button = QPushButton('📂 Abrir Archivo')
        self.file_button.setFixedSize(200, 50)
        self.model_button = QPushButton('🗃️ Cargar Modelo')
        self.model_button.setFixedSize(200, 50)
        self.path_label = QLabel('Ruta del archivo cargado:')

        # Tabla de datos
        self.table = DataTable()

        #Iniciamos el selector de columnas y la seccion de preprocesado
        self.init_selector()
        self.init_preprocess()
        
        self.connect_buttons()
        
        load_bar.addWidget(self.file_button)
        load_bar.addWidget(self.model_button)
        load_bar.addWidget(self.path_label)
        
        # Añadir todos los componentes al diseño principal
        layout.addWidget(self.load_widget)
        layout.addWidget(self.table)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.preprocess_label)
        layout.addWidget(self.preprocess_toolbar)

        self.setLayout(layout)

    def init_selector(self):
        # Selector de columnas (inicialmente oculto)
        self.column_selector = ColumnSelector()
        self.column_selector.setVisible(False)
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
        # Conectar botón de carga
        self.file_button.clicked.connect(self.load_data)
        self.model_button.clicked.connect(self.load_model)
        
        # Conectar botones de preprocesado
        self.preprocess_toolbar.buttons['delete'].clicked.connect(
            lambda: self.set_preprocessing_method('delete'))
        self.preprocess_toolbar.buttons['mean'].clicked.connect(
            lambda: self.set_preprocessing_method('mean'))
        self.preprocess_toolbar.buttons['median'].clicked.connect(
            lambda: self.set_preprocessing_method('median'))
        self.preprocess_toolbar.buttons['constant'].clicked.connect(
            self.handle_constant_method)
        self.preprocess_toolbar.apply_button.clicked.connect(
            self.apply_preprocessing)

    def load_model(self):
        model_path = open_file_dialog(self)
        if not model_path:
            return False

        try:
            #Cargar el modelo
            self.model = joblib.load(model_path)
            
            #Ocultar la tabla y el selector de columnas
            self.column_selector.setVisible(False)
            self.preprocess_label.hide()
            self.preprocess_toolbar.hide_buttons()
            
            #Mostrar la ruta del modelo cargado Y confirmación de la carga
            self.path_label.setText(
                f'📄 Ruta del modelo cargado: {model_path}')
            show_message('✅ ¡Modelo cargado exitosamente! 😃')

            self.display_model_data()

            return True
        
        except Exception as e:
            show_error(f'⚠ Error al cargar el modelo: {str(e)} ⚠')
            return False
        
    def display_model_data(self):
        """
        Displays the loaded model's data in the table.
        """
        try:
            if isinstance(self.model, dict):
                # Extraer y construir DataFrame con los datos del modelo
                data_dict = {
                    "Descripción": [
                        "Fórmula", "Intercepto", "Coeficientes", "Descripción",
                        "R²", "RMSE", "Columnas de Entrada", "Columna de Salida"
                    ],
                    "Valor": [
                        self.model.get("formula", "N/A"),
                        self.model.get("intercept", "N/A"),
                        ", ".join(map(str, self.model.get("coefficients", []))),
                        self.model.get("description", "Sin descripción"),
                        self.model.get("metrics", {}).get("r2_score", "N/A"),
                        self.model.get("metrics", {}).get("rmse", "N/A"),
                        ", ".join(self.model.get("columns", {}).get("input", [])),
                        self.model.get("columns", {}).get("output", "N/A")
                    ]
                }
                model_data_df = pd.DataFrame(data_dict)

                # Llama a update_data solo si el DataFrame tiene datos
                if model_data_df is not None and not model_data_df.empty:
                    self.table.update_data(model_data_df, model_data_df.shape[0])
                else:
                    show_error("⚠ El modelo no contiene datos válidos ⚠")
                    return False
                
                # Agregar el botón de predicción si no existe
                if not hasattr(self, "prediction_button"):
                    self.prediction_button = QPushButton('🔮 Realizar Predicción')
                    self.prediction_button.setFixedSize(200, 50)
                    self.prediction_button.setStyleSheet("font-size: 14px;")

                    # Asegurarse de que el botón "Realizar Predicción" sea visible
                    self.prediction_button.setVisible(True)

                    # Conectar el botón a un método de prueba
                    self.prediction_button.clicked.connect(self.make_a_prediction)

                    # Asegúrate de usar un layout válido
                    if self.layout() is None:
                        self.setLayout(QVBoxLayout())
                    
                    # Añade el botón al layout principal
                    self.layout().addWidget(self.prediction_button)
                
            else:
                show_error("⚠ Formato de modelo no soportado ⚠")
                return False
            
            return True
        except Exception as e:
            show_error(f'⚠ Error al mostrar los datos del modelo: {str(e)} ⚠')
            return False

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
            self.data = im.load_file(file_path)
            self.path_label.setText(
                f'📄 Ruta del archivo cargado: {file_path}')
            self.table.update_data(self.data, self.data.shape[0])
            self.column_selector.populate_columns(self.data.columns)
            self.column_selector.setVisible(True)
            show_message('✅ ¡Archivo cargado exitosamente! 😃')
                
        except Exception as e:
            show_error(f'⚠ Error al cargar el archivo: {str(e)} ⚠')

    def on_input_column_selection_changed(self, item):
        """
        Highlights a column in the table when it is selected or deselected
        in the column selector.

        Parameters
        ----------
        item : QListWidgetItem
            List item in `input_column_selector` that has changed state.
        """
        column_index = self.column_selector.input_column_selector.row(item)
        state = item.checkState()

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
        current_column_index = self.column_selector.output_column_selector.currentIndex()
        last_column_index = self.column_selector.output_column_selector.last_selected
        self.table.highlight_column(current_column_index, True)

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
        input_columns, output_column = self.column_selector.get_selected_columns()

        if not input_columns:
            show_error('⚠ Debe seleccionar al menos una columna de entrada. ⚠')
            return
        elif not output_column:
            show_error('⚠ Debe seleccionar una columna de salida. ⚠')
            return

        self.selected_input_columns = input_columns
        self.selected_output_column = output_column
        self.show_selection_summary(input_columns, output_column)
        if sum(map(int, none_count(self.data, input_columns + [output_column]))) > 0:
            self.enable_preprocessing() 

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
        show_message(summary)

    def enable_preprocessing(self):
        """
        Shows the preprocessing section in the interface, allowing the user
        to select and apply a preprocessing method.
        """
        self.preprocess_label.show()
        self.preprocess_toolbar.show_buttons()

    def handle_constant_method(self):
        """
        Shows an input dialog to define constant values by column
        when the user selects the constant preprocessing method.

        Notes
        -----
        This method only activates if input columns are selected.
        """
        if self.selected_input_columns:
            input_window = InputDialog(
                self.selected_input_columns + [self.selected_output_column],
                'Introduzca las constantes',
                parent = self
            )
            input_window.exec()
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
        """
        try:
            # Aplica el método de preprocesado y actualiza los datos
            self.preprocess_applier.apply_preprocess(
                self.data,
                self.selected_input_columns + [self.selected_output_column]
            )

            # Actualizar la tabla después de aplicar el preprocesado
            self.table.update_data(self.data, self.data.shape[0])

            # Repoblar el selector de columnas por si hay cambios en la estructura
            self.column_selector.populate_columns(self.data.columns)

            # Vuelve a seleccionar las columnas previamente seleccionadas
            for i in range(self.column_selector.input_column_selector.count()):
                item = self.column_selector.input_column_selector.item(i)
                if item.text() in self.selected_input_columns:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)

            last_selected = self.column_selector.output_column_selector.current_selection
            self.column_selector.output_column_selector.setCurrentIndex(last_selected)
            self.on_output_column_selection_changed()

            show_message('✅ ¡Preprocesado aplicado exitosamente!')
        except Exception as e:
            show_error(f'Error al aplicar el preprocesado: {str(e)}')


    def make_a_prediction(self):
        # Verificar si los datos están cargados correctamente
        if self.data is None:
            show_error('⚠ Los datos no están cargados. Por favor, cargue un archivo primero. ⚠')
            return
        
        # Obtener las columnas de entrada y salida del modelo cargado
        input_columns = self.model.get("columns", {}).get("input", [])
        output_column = self.model.get("columns", {}).get("output", "N/A")

        # Crear el objeto LinealModel si todo está bien
        try:
            self.lineal_model = LinealModel(self.data, input_columns, output_column)

            # Crear el objeto LinealModelTab
            self.lineal_model_tab = LinealModelTab(None, None, None)
            self.lineal_model_tab.model = self.lineal_model

            # Realizar la predicción
            self.lineal_model_tab.make_prediction()
            show_message('Predicción realizada con éxito!')
        
        except Exception as e:
            show_error(f'Error al realizar la predicción: {str(e)}')