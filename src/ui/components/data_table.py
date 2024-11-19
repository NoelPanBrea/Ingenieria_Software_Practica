from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QAbstractScrollArea, QStyledItemDelegate
from PyQt5.QtCore import Qt
import pandas as pd

class HighlightDelegate(QStyledItemDelegate):
    """
    Controls how cells are displayed in the table, particularly their highlighting.
    
    This delegate ensures that cell highlighting automatically adapts to the current
    application theme, maintaining visual consistency across different color schemes.
    """
    def initStyleOption(self, option, index):
        """
        Determines the visual style of each cell, applying highlighting when needed.
        Uses the application's current theme colors for consistency.
        """
        super().initStyleOption(option, index)
        if index.data(Qt.UserRole + 1):  # Check if cell should be highlighted
            option.backgroundBrush = option.palette.alternateBase()

class DataTable(QTableWidget):
    """
    Data table to display a subset of a `DataFrame` in a QTableWidget widget.

    This class provides functionalities to update and highlight columns based on 
    selected criteria.

    Parameters
    ----------
    parent : QWidget, optional
        The main widget containing the table, default is None.

    Attributes
    ----------
    table_data : pd.DataFrame
        DataFrame containing the data currently loaded into the table.

    Notes
    -----
    This widget does not allow direct data editing and automatically adjusts 
    column sizes to fit the content.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Sets up the initial properties of the table, such as size adjustment 
        and disabling direct editing.
        """
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setMinimumHeight(100)
        
        # Setup cell display handler
        self.setItemDelegate(HighlightDelegate())
        
        # Configure highlight color from current theme
        palette = self.palette()
        palette.setColor(palette.AlternateBase, self.palette().color(palette.Highlight).lighter(170))
        self.setPalette(palette)

    def update_data(self, data: pd.DataFrame, size: int):
        """
        Updates the table data with a subset of rows from the DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame containing the data to be displayed in the table.

        Notes
        -----
        Only half of the original DataFrame's rows are displayed to improve 
        efficiency and reduce visual load on the interface.
        """
        self.setRowCount(size)
        self.setColumnCount(data.shape[1])
        self.setHorizontalHeaderLabels(data.columns)
        
        #Definir precisión general para floats
        float_precision = 4
        
        for i in range(size):
            for j in range(data.shape[1]):
                cell_value = data.iat[i, j]
                # Formate si el valor es un float
                if isinstance(cell_value, float):
                    cell_value = f"{cell_value:.{float_precision}f}"
                item = QTableWidgetItem(str(cell_value))
                item.setData(Qt.UserRole + 1, False)  # Initialize unhighlighted
                self.setItem(i, j, item)
        
        self.resizeColumnsToContents()

    def highlight_column(self, column_index: int, highlight: bool):
        """
        Changes the background color of a specific column to highlight it.

        Parameters
        ----------
        column_index : int
            Index of the column to be highlighted.
        highlight : bool
            Indicates whether to apply or remove the highlight from the column.

        Notes
        -----
        Uses theme-aware colors for highlighting to maintain visual consistency
        """
        for row in range(self.rowCount()):
            if item := self.item(row, column_index):
                item.setData(Qt.UserRole + 1, highlight)
        self.viewport().update()