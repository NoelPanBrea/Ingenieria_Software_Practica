from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QListWidget, 
    QGridLayout, QListWidgetItem
)
from tabs.data_aux.combo_box import ComboBox
from PyQt5.QtCore import Qt
from typing import List

class ColumnSelector(QWidget):
    """
    Column selector for choosing input and output columns in a graphical interface.

    This widget allows users to select input columns (features) and an output column (target) 
    from a dataset. The user can select multiple input columns and confirm their selection.

    Parameters
    ----------
    parent : QWidget, optional
        The main widget that will contain the column selector, default is None.

    Attributes
    ----------
    Important Attributes
        input_column_selector : QListWidget
            List of available columns to select as input (features).
        output_column_selector : QComboBox
            Dropdown that displays available columns to choose the output column (target).
        confirm_button : QPushButton
            Button to confirm the column selection.
    
    Other Attributes
        input_label : QLabel
            Descriptive label for the input columns list.
        output_label : QLabel
            Descriptive label for selecting the output column.

    Notes
    -----
    It is important that the dataset column names are set before the user attempts selection. 
    This is achieved through the `populate_columns` method.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_column_selector = QListWidget()
        self.output_column_selector = ComboBox()
        self.confirm_button = QPushButton('Confirmar selección')
        self.init_ui()

    def init_ui(self):
        """
        Initializes the graphical interface for the column selector.

        Creates and organizes the `input_column_selector`, `output_column_selector`, 
        and `confirm_button` widgets, as well as the `input_label` and `output_label`.
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
        Populates the column selector with the dataset's column names.

        Parameters
        ----------
        columns : List[str]
            List of column names to populate the input and output selectors.

        Notes
        -----
        Call this method after loading the data to ensure that the column selector 
        shows the correct options.
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
        Gets the selected input and output columns.

        Returns
        -------
        tuple
            A tuple containing a list of selected input columns and a selected output column.

        Raises
        ------
        ValueError
            If no input or output column is selected.
        """
        input_columns = [
            self.input_column_selector.item(i).text()
            for i in range(self.input_column_selector.count())
            if self.input_column_selector.item(i).checkState() == Qt.Checked
        ]
        output_column = self.output_column_selector.currentText()
        return input_columns, output_column
