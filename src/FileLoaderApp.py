import sys
import import_module as im
from popup_handler import *
from dataset_calc import *
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHBoxLayout,
    QListWidget, QComboBox, QListWidgetItem, QGridLayout, QAbstractScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class FileLoaderApp(QWidget):
    def __init__(self) -> None:
        """
        Provides the object with attributes.

        Returns
        -----------
         None
        """
        super().__init__()
        self.data = None
        self.selected_input_columns = None
        self.preprocess_applier = PreprocessApplier()

        # inits the gui
        self.init_gui()

    def init_gui(self):
        """
        Inicializes the layouts and widgets of the GUI

        Returns
        -----------
         None
        """
        # main window config
        self.setWindowTitle('Linear regresion model maker')
        self.setGeometry(100, 100, 1200, 800)

        # GUI stylesheet
        stylesheet_doc = 'src/assets/stylesheet.txt'
        with open(stylesheet_doc) as stylesheet_doc:
            self.setStyleSheet(stylesheet_doc.read())

        # inits the main layout
        self.init_main_layout()

        # set the main layout
        self.setLayout(self.main_layout)

    def init_main_layout(self) -> None:
        self.main_layout = QVBoxLayout()
        self.tabs_init()
        self.main_layout.addWidget(self.tabs)

    def tabs_init(self) -> None:
        self.tabs = QTabWidget()
        self.data_tab_init()
        self.plot_tab_init()
        self.tabs.addTab(self.data_tab, 'Datos')
        self.tabs.addTab(self.plot_tab, 'Modelo')

    def plot_tab_init(self) -> None:
        self.plot_tab = QWidget()
        pass

    def data_tab_init(self) -> None:
        self.data_tab = QWidget()
        self.data_layout_init()
        self.data_tab.setLayout(self.data_layout)

    def data_layout_init(self) -> None:
        self.data_layout = QVBoxLayout()
        # inits the dependent layouts
        self.init_bar_layout()
        self.init_io_layout()
        self.init_preprocess_bar_layout()

        # layout elements are created
        res = 'Seleccione una opción de preprocesado de datos nulos:'
        self.apply_preprocess_label = QLabel(res)
        self.apply_preprocess_label.hide()
        # layout elements are added in order
        self.data_layout.addLayout(self.bar_layout)
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.table_widget.setMinimumHeight(100)
        self.data_layout.addWidget(self.table_widget)
        self.data_layout.addLayout(self.io_layout)
        self.data_layout.addWidget(self.apply_preprocess_label)
        self.data_layout.addLayout(self.preprocess_bar_layout)

    def init_bar_layout(self) -> None:
        self.bar_layout = QHBoxLayout()
        # layout elements are created
        self.file_path_label = QLabel('Ruta del archivo cargado:')
        self.load_button = QPushButton('📂 Abrir Archivo')
        self.load_button.setFixedWidth(200)
        self.load_button.setFixedHeight(50)
        self.load_button.clicked.connect(self.load_button_handle)

        # layout elements are added in order
        self.bar_layout.addWidget(self.load_button)
        self.bar_layout.addWidget(self.file_path_label)

    def init_io_layout(self) -> None:
        self.io_layout = QGridLayout()
        res = 'Seleccione columnas de entrada (features):'
        self.input_label = QLabel(res)
        self.input_column_selector = QListWidget()
        self.input_column_selector.setMaximumHeight(100)
        self.input_column_selector.setMaximumWidth(self.width() // 2)
        self.input_column_selector.setMinimumWidth(self.height() // 2)
        self.output_label = QLabel('Seleccione columna de salida (target):')
        self.input_column_selector.itemChanged.connect(
            self.on_checkbox_changed)
        self.input_label.hide()
        self.input_column_selector.hide()
        self.output_label.hide()

        # dependent layouts are inicialized
        self.init_io_inside_layout()
        self.io_layout.addWidget(
            self.input_label, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        self.io_layout.addWidget(self.output_label, 0,
                                 1, alignment=Qt.AlignmentFlag.AlignBottom)
        self.io_layout.addWidget(
            self.input_column_selector, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.io_layout.addLayout(
            self.io_inside_layout, 1, 1, Qt.AlignmentFlag.AlignTop)

    def init_preprocess_bar_layout(self):
        self.preprocess_bar_layout = QHBoxLayout()
        buttons = ['Eliminar', 'Media', 'Mediana', 'Constantes']
        functions = [self.delete, self.mean, self.median, self.constant]
        self.preproces_buttons = []
        self.apply_button = QPushButton('Aplicar preprocesado')
        self.apply_button.hide()
        self.apply_button.clicked.connect(self.apply)
        self.apply_button.setMinimumWidth(400)
        for name, function in zip(buttons, functions):
            widget = QPushButton(name)
            widget.hide()
            widget.clicked.connect(function)
            self.preproces_buttons.append(widget)
            self.preprocess_bar_layout.addWidget(widget)
        self.preprocess_bar_layout.addWidget(self.apply_button)

    def init_io_inside_layout(self) -> None:
        self.io_inside_layout = QVBoxLayout()
        self.output_column_selector = QComboBox()
        self.confirm_button = QPushButton('Confirmar selección')
        self.output_column_selector.hide()
        self.confirm_button.hide()
        self.confirm_button.clicked.connect(self.confirm_button_handle)

        self.io_inside_layout.addWidget(self.output_column_selector)
        self.io_inside_layout.addWidget(self.confirm_button)

    def delete(self) -> None:
        """
        Sets the Qaction Action1 function
        Returns
        -----------
         None
        """
        self.preprocess_applier.set_current_method('delete')

    def apply(self) -> None:
        """
        Sets the Qaction Action2 function
        Returns
        -----------
         None
        """
        try:
            self.preprocess_applier.apply_preprocess(self.data,
                                                     self.selected_input_columns)
        except Exception as e:
            show_error(f'Error al aplicar el preprocesado: {str(e)}')
        self.reload_table()
        for x in range(self.input_column_selector.count()):
            self.on_checkbox_changed(self.input_column_selector.item(x))

    def mean(self) -> None:
        """
        Sets the Qaction mean function

        Returns
        -----------
         None
        """
        self.preprocess_applier.set_current_method('mean')

    def median(self) -> None:
        """
        Sets the Qaction median function

        Returns
        -----------
         None
        """
        self.preprocess_applier.set_current_method('median')

    def constant(self) -> None:
        """
        Sets the Qaction constant function

        Returns
        -----------
         None
        """
        if self.selected_input_columns:
            input_window = InputDialog(self.selected_input_columns,
                                       'Introduzca las constantes', self.styleSheet())
            input_window.exec()
            constants = input_window.get_inputs()
            self.preprocess_applier.set_current_method('constant', constants)

    def load_button_handle(self) -> None:
        file_path = open_file_dialog(self)
        if file_path:
            self.file_path_label.setText(
                f'📄 Ruta del archivo cargado: {file_path}')
            self.display_data(file_path)

    def display_data(self, file_path) -> None:
        """
        Loads the data and displays them in a table

        Returns
        -----------
         None
        """
        try:
            self.data = im.load_file(file_path)
            # Mostrar los datos en la tabla
            self.reload_table()
            # Habilitar los selectores de columnas y mostrarlos
            self.enable_selectors(self.data.columns)
            # Mensaje de éxito
            show_message('✅ ¡Archivo cargado exitosamente! 😃')
        except Exception as e:
            show_error(f'⚠ Error al cargar el archivo: {str(e)} ⚠')

    def reload_table(self) -> None:
        """
        Reloads the tablewidget to update it to the current dataset

        Returns
        -----------
         None
        """
        self.table_widget.setRowCount(self.data.shape[0] // 2)
        self.table_widget.setColumnCount(self.data.shape[1])
        self.table_widget.setHorizontalHeaderLabels(self.data.columns)

        for i in range(self.data.shape[0] // 2):
            for j in range(self.data.shape[1]):
                self.table_widget.setItem(
                    i, j, QTableWidgetItem(str(self.data.iat[i, j])))
        self.table_widget.resizeColumnsToContents()

    def enable_selectors(self, columns) -> None:
        """
        Enables the column selectors with checkboxes for the input columns
        and a dropbox for the output column

        Returns
        -----------
         None
        """
        self.input_column_selector.clear()
        self.output_column_selector.clear()

        # Mostrar selectores y botones
        self.input_label.show()
        self.input_column_selector.show()
        self.output_label.show()
        self.output_column_selector.show()
        self.confirm_button.show()

        # Agregar checkboxes a las columnas de entrada
        for column in columns:
            item = QListWidgetItem(column)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)  # Checkbox no marcado por defecto
            self.input_column_selector.addItem(item)

        # Agregar opciones al selector de columna de salida
        self.output_column_selector.addItems(columns)

        # Habilitar botones
        self.confirm_button.setEnabled(True)

    def on_checkbox_changed(self, item):
        """
        Changes the color of the corresponding columns as it is selected
        or deselected

        Returns
        -----------
         None
        """
        column_index = self.input_column_selector.row(
            item)  # Obtener el índice de la columna
        if item.checkState() == Qt.Checked:
            # Cambiar color de la columna a naranja
            for row in range(self.table_widget.rowCount()):
                self.table_widget.item(row, column_index).setBackground(
                    QColor(255, 171, 130))  # Color naranja 147
        else:
            # Restaurar color de la columna a blanco
            for row in range(self.table_widget.rowCount()):
                self.table_widget.item(row, column_index).setBackground(
                    QColor(255, 243, 224))

    def confirm_button_handle(self) -> None:
        self.confirm_selection()
        if self.selected_input_columns:
            self.apply_preprocess_label.show()
            self.apply_button.show()
            for widgets in self.preproces_buttons:
                widgets.show()

    def confirm_selection(self) -> None:
        """
        Applies the column selection and shows a message with the selection

        Returns
        -----------
         None
        """
        self.selected_input_columns = [self.input_column_selector.item(i).text()
                                       for i in range(self.input_column_selector.count())
                                       if self.input_column_selector.item(i).checkState() == Qt.Checked]
        self.output_column = self.output_column_selector.currentText()

        if not self.selected_input_columns:
            show_error(
                '⚠ Debe seleccionar al menos una columna de entrada. ⚠')
        elif self.output_column == '':
            show_error('⚠ Debe seleccionar una columna de salida. ⚠')
        else:
            res = f'Columnas de entrada: {
                ', '.join(self.selected_input_columns)}'
            res += f'\nValores nulos: {', '.join(
                map(str, none_count(self.data, self.selected_input_columns)))}'
            res += f'\nColumna de salida: {self.output_column} '
            show_message(res)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileLoaderApp()
    ex.show()
    sys.exit(app.exec_())
