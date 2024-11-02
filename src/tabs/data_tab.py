from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt
from typing import List, Optional
import pandas as pd

import tabs.data_aux.import_module as im
from tabs.data_aux.popup_handler import *
from tabs.data_aux.dataset_calc import *
from tabs.data_aux.column_selector import ColumnSelector
from tabs.data_aux.data_table import DataTable
from tabs.data_aux.preprocess_toolbar import PreprocessToolbar

class DataTab(QWidget):
    """
    Pestaña de datos que administra la carga, selección y preprocesado de datos.

    Esta clase organiza los elementos de la interfaz gráfica relacionados con
    la carga de archivos, selección de columnas y opciones de preprocesado,
    facilitando la interacción con el usuario y la aplicación de operaciones en
    un DataFrame.

    Attributes
    ----------
    data : pd.DataFrame, optional
        El DataFrame que contiene los datos cargados.
    selected_input_columns : List[str], optional
        Lista de columnas seleccionadas como entradas para el análisis.
    preprocess_applier : PreprocessApplier
        Objeto para gestionar y aplicar el método de preprocesado seleccionado.
    load_button : QPushButton
        Botón para abrir un archivo de datos.
    file_path_label : QLabel
        Etiqueta que muestra la ruta del archivo cargado.
    table : DataTable
        Tabla que muestra una vista previa de los datos cargados.
    column_selector : ColumnSelector
        Selector de columnas para elegir las columnas de entrada y salida.
    preprocess_label : QLabel
        Etiqueta que describe las opciones de preprocesado.
    preprocess_toolbar : PreprocessToolbar
        Barra de herramientas con botones de opciones de preprocesado.

    Notes
    -----
    Asegúrate de que `PreprocessApplier` y `import_module` estén implementados
    correctamente para que los métodos de preprocesado funcionen como se espera.
    """

    def __init__(self):
        super().__init__()
        self.data: Optional[pd.DataFrame] = None
        self.selected_input_columns: Optional[List[str]] = None
        self.preprocess_applier = PreprocessApplier()
        self.init_ui()

    def init_ui(self):
        """
        Inicializa la interfaz gráfica de la pestaña de datos, incluyendo botones,
        etiquetas y tablas para la carga de datos y la selección de preprocesado.
        """
        layout = QVBoxLayout()

        # Sección de carga de archivo
        file_bar = QHBoxLayout()
        self.load_button = QPushButton('📂 Abrir Archivo')
        self.load_button.setFixedSize(200, 50)
        self.load_button.clicked.connect(self.load_data)
        self.file_path_label = QLabel('Ruta del archivo cargado:')
        file_bar.addWidget(self.load_button)
        file_bar.addWidget(self.file_path_label)

        # Tabla de datos
        self.table = DataTable()

        # Selector de columnas (inicialmente oculto)
        self.column_selector = ColumnSelector()
        self.column_selector.setVisible(False)
        self.column_selector.confirm_button.clicked.connect(
            self.on_selection_confirmed)
        self.column_selector.input_column_selector.itemChanged.connect(
            self.on_column_selection_changed)

        # Sección de preprocesado
        self.preprocess_label = QLabel(
            'Seleccione una opción de preprocesado de datos nulos:')
        self.preprocess_label.hide()
        self.preprocess_toolbar = PreprocessToolbar()

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

        # Añadir todos los componentes al diseño principal
        layout.addLayout(file_bar)
        layout.addWidget(self.table)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.preprocess_label)
        layout.addWidget(self.preprocess_toolbar)

        self.setLayout(layout)

    def load_data(self):
        """
        Carga un archivo de datos seleccionado por el usuario, actualizando la
        tabla y el selector de columnas.

        Notes
        -----
        Utiliza `im.load_file` para cargar el archivo y `show_message` para
        informar al usuario en caso de éxito o error.
        """
        file_path = open_file_dialog(self)
        if not file_path:
            return

        try:
            self.data = im.load_file(file_path)
            self.file_path_label.setText(
                f'📄 Ruta del archivo cargado: {file_path}')
            self.table.update_data(self.data)
            self.column_selector.populate_columns(self.data.columns)
            self.column_selector.setVisible(True)
            show_message('✅ ¡Archivo cargado exitosamente! 😃')
        except Exception as e:
            show_error(f'⚠ Error al cargar el archivo: {str(e)} ⚠')

    def on_column_selection_changed(self, item):
        """
        Resalta una columna en la tabla cuando se selecciona o deselecciona
        en el selector de columnas.

        Parameters
        ----------
        item : QListWidgetItem
            Elemento de la lista en `input_column_selector` que ha cambiado de estado.
        """
        column_index = self.column_selector.input_column_selector.row(item)
        self.table.highlight_column(
            column_index, item.checkState() == Qt.Checked)

    def on_selection_confirmed(self):
        """
        Confirma las columnas seleccionadas por el usuario y activa la
        interfaz de preprocesado.

        Raises
        ------
        ValueError
            Si no se seleccionan columnas de entrada o una columna de salida.
        """
        input_columns, output_column = self.column_selector.get_selected_columns()

        if not input_columns:
            show_error('⚠ Debe seleccionar al menos una columna de entrada. ⚠')
            return
        elif not output_column:
            show_error('⚠ Debe seleccionar una columna de salida. ⚠')
            return

        self.selected_input_columns = input_columns
        self.show_selection_summary(input_columns, output_column)
        self.enable_preprocessing()

    def set_preprocessing_method(self, method: str):
        """
        Define el método de preprocesado actual y muestra el botón 'Aplicar'.

        Parameters
        ----------
        method : str
            Método de preprocesado a aplicar ('delete', 'mean', 'median', 'constant').
        """
        self.preprocess_applier.set_current_method(method)

    def show_selection_summary(self, input_columns: List[str], output_column: str):
        """
        Muestra un resumen de las columnas seleccionadas en un mensaje emergente.

        Parameters
        ----------
        input_columns : List[str]
            Lista de nombres de columnas seleccionadas como entrada.
        output_column : str
            Nombre de la columna seleccionada como salida.
        """
        summary = (
            f'Columnas de entrada: {", ".join(input_columns)}\n'
            f'Valores nulos: {
                ", ".join(map(str, none_count(self.data, input_columns)))}\n'
            f'Columna de salida: {output_column}'
        )
        show_message(summary)

    def enable_preprocessing(self):
        """
        Muestra la sección de preprocesado en la interfaz, permitiendo al usuario
        seleccionar y aplicar un método de preprocesado.
        """
        self.preprocess_label.show()
        self.preprocess_toolbar.show_buttons()

    def handle_constant_method(self):
        """
        Muestra un diálogo de entrada para definir valores constantes por columna
        cuando el usuario selecciona el método de preprocesado de constante.

        Notes
        -----
        Este método solo se activa si hay columnas de entrada seleccionadas.
        """
        if self.selected_input_columns:
            input_window = InputDialog(
                self.selected_input_columns,
                'Introduzca las constantes',
                self.styleSheet()
            )
            input_window.exec()
            constants = input_window.get_inputs()
            self.preprocess_applier.set_current_method('constant', constants)

    def apply_preprocessing(self):
        """
        Aplica el método de preprocesado seleccionado a los datos cargados
        y actualiza la tabla y el selector de columnas.

        Raises
        ------
        Exception
            Si ocurre un error durante el preprocesado de datos.
        """
        try:
            # Aplica el método de preprocesado y actualiza los datos
            self.preprocess_applier.apply_preprocess(
                self.data,
                self.selected_input_columns
            )

            # Actualizar la tabla después de aplicar el preprocesado
            self.table.update_data(self.data)

            # Repoblar el selector de columnas por si hay cambios en la estructura
            self.column_selector.populate_columns(self.data.columns)

            # Vuelve a seleccionar las columnas previamente seleccionadas
            for i in range(self.column_selector.input_column_selector.count()):
                item = self.column_selector.input_column_selector.item(i)
                if item.text() in self.selected_input_columns:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)

            show_message('✅ ¡Preprocesado aplicado exitosamente!')
        except Exception as e:
            show_error(f'Error al aplicar el preprocesado: {str(e)}')