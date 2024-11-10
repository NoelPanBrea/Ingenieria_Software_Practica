from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QListWidget, 
    QGridLayout, QListWidgetItem
)
from tabs.data_aux.combo_box import ComboBox
from PyQt5.QtCore import Qt
from typing import List

class ColumnSelector(QWidget):
    """
    Selector de columnas para elegir columnas de entrada y salida en una interfaz gráfica.

    Este widget permite a los usuarios seleccionar columnas de entrada (features) y una columna
    de salida (target) a partir de un conjunto de datos. El usuario puede seleccionar múltiples
    columnas de entrada y confirmar su selección.

    Parameters
    ----------
    parent : QWidget, optional
        El widget principal que contendrá al selector de columnas, por defecto None.

    Attributes
    ----------
    Important Attributes
        input_column_selector : QListWidget
            Lista de columnas disponibles para seleccionar como entrada (features).
        output_column_selector : QComboBox
            Desplegable que muestra las columnas disponibles para elegir la columna de salida (target).
        confirm_button : QPushButton
            Botón para confirmar la selección de columnas.
    
    Other Attributes
        input_label : QLabel
            Etiqueta descriptiva para la lista de columnas de entrada.
        output_label : QLabel
            Etiqueta descriptiva para la selección de columna de salida.

    Notes
    -----
    Es importante que los nombres de columna del dataset se establezcan antes de que el usuario
    intente realizar la selección. Esto se logra a través del método `populate_columns`.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_column_selector = QListWidget()
        self.output_column_selector = ComboBox()
        self.confirm_button = QPushButton('Confirmar selección')
        self.init_ui()

    def init_ui(self):
        """
        Inicializa la interfaz gráfica del selector de columnas.

        Crea y organiza los widgets `input_column_selector`, `output_column_selector`, `confirm_button`,
        así como las etiquetas `input_label` y `output_label`.
        """
        layout = QGridLayout()

        self.input_label = QLabel('Seleccione columnas de entrada (features):')
        self.output_label = QLabel('Seleccione columna de salida (target):')
        self.input_column_selector.setMinimumHeight(150)
        self.input_column_selector.setMaximumHeight(250)
        self.confirm_button.setMinimumHeight(150)

        layout.addWidget(self.input_label, 0, 0,
                         alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.output_label, 0, 1,
                         alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.input_column_selector, 1, 0,
                         alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.output_column_selector, 1, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.confirm_button, 1, 2, Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

    def populate_columns(self, columns: List[str]):
        """
        Pobla el selector de columnas con los nombres de las columnas del dataset.

        Parameters
        ----------
        columns : List[str]
            Lista de nombres de columnas para poblar los selectores de entrada y salida.

        Notes
        -----
        Llama a este método después de cargar los datos para asegurarse de que el selector
        de columnas muestre las opciones correctas.
        """
        self.input_column_selector.clear()
        self.output_column_selector.clear()

        for column in columns:
            item = QListWidgetItem(column)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.input_column_selector.addItem(item)

        self.output_column_selector.addItems(columns)
        self.output_column_selector.setCurrentIndex(-1)

    def get_selected_columns(self) -> tuple:
        """
        Obtiene las columnas seleccionadas como entrada y salida.

        Returns
        -------
        tuple
            Una tupla que contiene una lista de columnas seleccionadas como entrada 
            y una columna de salida seleccionada.

        Raises
        ------
        ValueError
            Si no hay ninguna columna seleccionada como entrada o salida.
        """
        input_columns = [
            self.input_column_selector.item(i).text()
            for i in range(self.input_column_selector.count())
            if self.input_column_selector.item(i).checkState() == Qt.Checked
        ]
        output_column = self.output_column_selector.currentText()
        return input_columns, output_column
