import sys
import import_module as im
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMenu, QInputDialog, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QMessageBox, QHBoxLayout, QListWidget, QComboBox,
    QListWidgetItem, QGridLayout
)
from PyQt5.QtCore import Qt, QPoint
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
        self.initUI()
        self.data = None
        self.selected_input_columns = None
        self.preproces_config = None

    def initUI(self):
        """
        Configura la interfaz gráfica de usuario (GUI) de la aplicación.

        Returns
        -----------
         None
        """
        # Configuración de la ventana principal
        self.setWindowTitle('Lectura de Datasets - GUI')
        self.setGeometry(100, 100, 1200, 800)  # Ventana más grande

        # Estilos de la interfaz gráfica
        stylesheet_doc = 'src/assets/stylesheet.txt'
        with open(stylesheet_doc) as stylesheet_doc:
            self.setStyleSheet(stylesheet_doc.read())

        # Layout principal
        main_layout = QVBoxLayout()
        bar_layout = QHBoxLayout()
        io_layout = QGridLayout()
        io_inside_layout = QVBoxLayout()


        # Botón para cargar archivos
        self.load_button = QPushButton('📂 Abrir Archivo')
        self.load_button.setFixedWidth(200)
        self.load_button.setFixedHeight(50)
        self.load_button.clicked.connect(self.open_file_dialog)

        # Botón para desplegar menú de configuración de preprocesado
        self.config_button = QPushButton('⚙️ Configuración')
        self.config_button.setFixedHeight(50)
        self.config_button.setFixedWidth(200)
        self.config_button.clicked.connect(self.pop_up_menu)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.file_path_label = QLabel('Ruta del archivo cargado:')

        bar_layout.addWidget(self.load_button)
        bar_layout.addWidget(self.file_path_label)
        bar_layout.addWidget(self.config_button)
        main_layout.addLayout(bar_layout)
        # Tabla para mostrar los datos
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setMinimumHeight(100)
        main_layout.addWidget(self.table_widget)

        # Selectores de columnas (inicialmente ocultos)
        res = 'Seleccione columnas de entrada (features):'
        self.input_label = QLabel(res)
        self.input_column_selector = QListWidget()
        # Altura mínima reducida para usar menos espacio
        self.input_column_selector.setMinimumHeight(150)
        self.input_column_selector.setMaximumHeight(
            250)  # Altura máxima reducida
        self.input_column_selector.setMinimumWidth(
            self.height() // 2)  
        self.output_label = QLabel('Seleccione columna de salida (target):')
        self.output_column_selector = QComboBox()
        self.confirm_button = QPushButton('Confirmar selección')
        self.confirm_button.setMaximumHeight(100)
        # Ocultar estos elementos inicialmente
        self.input_label.hide()
        self.input_column_selector.hide()
        self.output_label.hide()
        self.output_column_selector.hide()
        self.confirm_button.hide()

        # Conectar el cambio de estado del checkbox al método correspondiente
        self.input_column_selector.itemChanged.connect(
            self.on_checkbox_changed)

        # Agregar al layout pero ocultos
        io_layout.addWidget(self.input_label, 0, 0, alignment = Qt.AlignmentFlag.AlignBottom)
        io_layout.addWidget(self.output_label, 0, 1, alignment = Qt.AlignmentFlag.AlignBottom)
        io_layout.addWidget(self.input_column_selector, 1, 0, alignment = Qt.AlignmentFlag.AlignTop)
        io_layout.addLayout(io_inside_layout, 1, 1, Qt.AlignmentFlag.AlignTop)
        io_inside_layout.addWidget(self.output_column_selector)
        io_inside_layout.addWidget(self.confirm_button)
        main_layout.addLayout(io_layout)
        
 

        # Conectar el botón de confirmación con la función confirm_selection
        self.confirm_button.clicked.connect(self.confirm_selection)
        # Menu preconfiguración de los datos
        self.menu = QMenu(self)
        action1 = self.menu.addAction('Eliminar datos nulos')
        sub_menu = self.menu.addMenu('Sustituir datos nulos')
        action2 = self.menu.addAction('Aplicar cambios')
        subaction1_1 = sub_menu.addAction('Media')
        subaction1_2 = sub_menu.addAction('Mediana')
        subaction1_3 = sub_menu.addAction('Constante')
        action1.triggered.connect(self.action1_handle)
        action2.triggered.connect(self.action2_handle)
        subaction1_1.triggered.connect(self.subaction1_1_handle)
        subaction1_2.triggered.connect(self.subaction1_2_handle)
        subaction1_3.triggered.connect(self.subaction1_3_handle)

        # Asignar layout principal
        self.setLayout(main_layout)

    def init_bar_layout(self) -> list:
        # Botón para cargar archivos
        self.load_button = QPushButton('📂 Abrir Archivo')
        self.load_button.setFixedWidth(200)
        self.load_button.setFixedHeight(50)
        self.load_button.clicked.connect(self.open_file_dialog)

        # Botón para desplegar menú de configuración de preprocesado
        self.config_button = QPushButton('⚙️ Configuración')
        self.config_button.setFixedHeight(50)
        self.config_button.setFixedWidth(200)
        self.config_button.clicked.connect(self.pop_up_menu)

        widgets = [self.config_button, self.load_button]
        return  widgets

    def init_main_layout(self):
        for layout in self.init_main_layout_l():
            self.init_main_layout_w()

    def init_main_layout_l(self):
        # Layout para botones de barra de herramientas
        bar_layout = QHBoxLayout()
        for widget in self.init_bar_layout():
            bar_layout.addWidget(widget)
        return  bar_layout
    
    def init_main_layout_w(self):
        # Botón para confirmar la selección de columnas
        self.confirm_button = QPushButton('Confirmar selección')
        self.confirm_button.hide()
        self.confirm_button.clicked.connect(self.confirm_selection)


        widgets = [self.confirm_button]
        return  widgets

    def action1_handle(self) -> None:
        """
        Sets the Qaction Action1 function
        Returns
        -----------
         None
        """
        self.preproces_config = 'Delete'

    def action2_handle(self) -> None:
        """
        Sets the Qaction Action2 function
        Returns
        -----------
         None
        """
        self.apply_preproces()

    def subaction1_1_handle(self) -> None:
        """
        Sets the Qaction subaction1_1 function

        Returns
        -----------
         None
        """
        self.preproces_config = 'Mean'

    def subaction1_2_handle(self) -> None:
        """
        Sets the Qaction subaction1_2 function

        Returns
        -----------
         None
        """
        self.preproces_config = 'Median'

    def subaction1_3_handle(self) -> None:
        """
        Sets the Qaction subaction1_3 function

        Returns
        -----------
         None
        """
        input_window = QInputDialog(self)
        constants = input_window.getText(self,
                                         'Introduzca el valor de las constantes',
                                         'Constantes separadas por espacios')
        self.preproces_config = ('Cte', constants) if constants[1] else None

    def pop_up_menu(self) -> None:
        """
        Launches the pop_up_menu

        Returns
        -----------
         None
        """
        pos = self.config_button.mapToGlobal(QPoint(0, 50))
        self.menu.exec_(pos)

    def none_count(self) -> list[int]:
        """
        Counts the None values of the columns in selected_input_columns

        Returns
        -----------
        [self.data[x].isna().sum() for\
                x in self.selected_input_columns]: list[int]
                List with the number of None values of the selected columns
        """
        return [self.data[x].isna().sum() for
                x in self.selected_input_columns]

    def apply_preproces(self) -> None:
        """
        Modifies the value of Nones according to the current configuration

        Returns
        -----------
         None
        """
        if self.selected_input_columns is not None\
                and self.preproces_config is not None:
            if self.preproces_config == 'Delete':
                self.data = self.data.dropna(
                    subset=self.selected_input_columns)
            elif self.preproces_config == 'Mean':
                for x in self.selected_input_columns:
                    self.data[x] = self.data[x].fillna(
                        self.data[x].mean(skipna=True))
            elif self.preproces_config == 'Median':
                for x in self.selected_input_columns:
                    self.data[x] = self.data[x].fillna(
                        self.data[x].median(skipna=True))
            elif self.preproces_config[0] == 'Cte':
                try:
                    numbers = self.preproces_config[1][0].split(' ')
                    if len(self.selected_input_columns) != len(numbers):
                        res = 'El número de constantes ha de ser '
                        res += 'igual al de columnas seleccionadas'
                        raise ValueError(res)
                    for i, x in enumerate(self.selected_input_columns):
                        self.data[x] = self.data[x].fillna(float(numbers[i]))
                except Exception as e:
                    self.show_error(f'Se produjo un error inesperado: {e}')
            self.reload_table()

    def open_file_dialog(self) -> None:
        """
        Shows the dialog to open files and loads the selected file

        Returns
        -----------
         None
        """
        options = QFileDialog.Options()
        res = 'Todos los Archivos (*.*);;Archivos CSV (*.csv);;Archivos Excel'
        res += ' (*.xlsx *.xls);;Base de datos SQLite (*.sqlite *.db)'
        file_path, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo',
            '', res, options=options)

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
            self.show_message('✅ ¡Archivo cargado exitosamente! 😃')
        except Exception as e:
            self.show_error(f'⚠ Error al cargar el archivo: {str(e)} ⚠')

    def reload_table(self) -> None:
        """
        Reloads the tablewidget to update it to the current dataset

        Returns
        -----------
         None
        """
        self.table_widget.setRowCount(self.data.shape[0])
        self.table_widget.setColumnCount(self.data.shape[1])
        self.table_widget.setHorizontalHeaderLabels(self.data.columns)

        for i in range(self.data.shape[0]):
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
        for index, column in enumerate(columns):
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
                    QColor(255, 171, 145))  # Color naranja
        else:
            # Restaurar color de la columna a blanco
            for row in range(self.table_widget.rowCount()):
                self.table_widget.item(row, column_index).setBackground(
                    QColor(255, 243, 224))

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
            self.show_error(
                '⚠ Debe seleccionar al menos una columna de entrada. ⚠')
        elif self.output_column == '':
            self.show_error('⚠ Debe seleccionar una columna de salida. ⚠')
        else:
            self.show_message(f'Columnas de entrada: {', '.join(
                self.selected_input_columns)}\nValores nulos: {', '.join(
                    map(str, self.none_count()))}\nColumna de salida: {self.output_column} ')

    def show_message(self, message: str) -> None:
        """
        Shows a message in a pop up window

        Parameters 
        -----------
        message : str
            String to show in the pop up

        Returns
        -----------
         None
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Éxito")
        msg_box.exec_()

    def show_error(self, message: str) -> None:
        """
        Shows an error message in a pop up window

        Parameters 
        -----------
        message : str
            Error string to show in the pop up

        Returns
        -----------
         None
        """
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setText(message)
        error_msg.setWindowTitle('Error')
        error_msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileLoaderApp()
    ex.show()
    sys.exit(app.exec_())
