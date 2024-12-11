from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QAbstractScrollArea, QStyledItemDelegate
from PyQt5.QtCore import Qt, QTimer
from pandas import DataFrame


class HighlightDelegate(QStyledItemDelegate):
    """
    Controls how cells are displayed in the table, particularly their highlighting.
    """
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.data(Qt.UserRole + 1):  # Check if cell should be highlighted
            option.backgroundBrush = option.palette.alternateBase()


class DataTable(QTableWidget):
    """
    _data table with lazy loading for large DataFrames.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self._data = None  # Full DataFrame
        self.loaded_rows = 0  # Rows currently loaded
        self.batch_size = 100  # Number of rows to load at a time

    @property
    def data(self) -> DataFrame:
        """
        Returns the DataFrame with the table data

        Returns
        ----------
        self._data : DataFrame
                DataFrame with the current table data 
        """
        return self._data

    def init_ui(self):
        """
        Sets up initial table properties and connects scroll events.
        """
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setMinimumHeight(300)

        # Setup cell display handler
        self.setItemDelegate(HighlightDelegate())
        self.verticalScrollBar().valueChanged.connect(self.on_scroll)

    def load_data(self, data: DataFrame, batch_size: int = 100):
        """
        Initializes the table with _data for lazy loading.

        Parameters
        ----------
        _data : DataFrame
            The DataFrame to be loaded lazily.
        batch_size : int
            Number of rows to load per batch.
        """
        self._data = data
        self.batch_size = batch_size
        self.loaded_rows = 0

        # Setup table headers
        self.setColumnCount(self._data.shape[1])
        self.setHorizontalHeaderLabels(self._data.columns)

        # Load initial rows
        self.load_more_rows()

    def load_more_rows(self):
        """
        Loads the next batch of rows into the table.
        """
        if self._data is None:
            return

        # Determine the next range of rows to load
        start_row = self.loaded_rows
        end_row = min(self.loaded_rows + self.batch_size, len(self._data))

        if start_row >= end_row:  # No more rows to load
            return

        self.setRowCount(end_row)  # Extend the table to accommodate new rows

        # Load rows into the table
        float_precision = 4
        for i in range(start_row, end_row):
            for j in range(self._data.shape[1]):
                cell_value = self._data.iat[i, j]
                # Format float values
                if isinstance(cell_value, float):
                    cell_value = f"{cell_value:.{float_precision}f}"
                item = QTableWidgetItem(str(cell_value))
                item.setData(Qt.UserRole + 1, False)  # Initialize unhighlighted
                self.setItem(i, j, item)

        self.loaded_rows = end_row
        self.highlight_check()
        self.resizeColumnsToContents()
        self.fill_area(self._data.shape[1])

    def on_scroll(self):
        """
        Checks if the user has scrolled near the bottom to load more rows.
        """
        scroll_bar = self.verticalScrollBar()
        if scroll_bar.value() > scroll_bar.maximum() - 50:  # Threshold for loading
            QTimer.singleShot(50, self.load_more_rows)

    def highlight_check(self):
        for col in range(self.columnCount()):
            if self.item(0, col).data(Qt.UserRole + 1):
                self.highlight_column(col, True)

    def highlight_column(self, column_index: int, highlight: bool):
        """
        Highlights a specific column in the table.
        """
        for row in range(self.rowCount()):
            if item := self.item(row, column_index):
                item.setData(Qt.UserRole + 1, highlight)
        self.viewport().update()

    def columns_width(self) -> int:
        """
        Returns the sum of the column's width
        """
        return sum([self.columnWidth(i) for i in range(self.data.shape[1])])

    def fill_area(self, shape) -> None:
        """
        Adjusts the column width to the table's width
        """
        width = self.width()
        shape = self.data.shape[1]
        if self.columns_width() < width:
            for i in range(shape):
                self.setColumnWidth(i, width // shape)