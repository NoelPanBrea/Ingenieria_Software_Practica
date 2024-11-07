from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QAbstractScrollArea
from PyQt5.QtGui import QColor
import pandas as pd

class DataTable(QTableWidget):
    """
    Tabla de datos para mostrar un subconjunto de datos de un `DataFrame` en un widget QTableWidget.

    La clase proporciona funcionalidades para actualizar y resaltar columnas en función de
    criterios seleccionados.

    Parameters
    ----------
    parent : QWidget, optional
        El widget principal que contiene la tabla, por defecto None.

    Attributes
    ----------
    table_data : pd.DataFrame
        DataFrame que contiene los datos actualmente cargados en la tabla.

    Notes
    -----
    Este widget no permite la edición directa de los datos y ajusta automáticamente el tamaño
    de las columnas para adaptarse al contenido.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Configura las propiedades iniciales de la tabla, como el ajuste de tamaño
        y la desactivación de edición directa.
        """
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setMinimumHeight(100)

    def update_data(self, data: pd.DataFrame, size: int):
        """
        Actualiza los datos de la tabla con un subconjunto de filas del DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            El DataFrame con los datos que se mostrarán en la tabla.

        Notes
        -----
        Solo se muestra la mitad de las filas del DataFrame original para mejorar
        la eficiencia y reducir la carga visual en la interfaz.
        """
        shown_rows = size if size >= data.shape[0] else data.shape[0]

        self.setRowCount(shown_rows)
        self.setColumnCount(data.shape[1])
        self.setHorizontalHeaderLabels(data.columns)

        for i in range(shown_rows):
            for j in range(data.shape[1]):
                self.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))
        self.resizeColumnsToContents()

    def highlight_column(self, column_index: int, highlight: bool):
        """
        Cambia el color de fondo de una columna específica para resaltarla.

        Parameters
        ----------
        column_index : int
            Índice de la columna que se desea resaltar.
        highlight : bool
            Indica si se debe aplicar o quitar el resaltado de la columna.

        Notes
        -----
        El color del resaltado es fijo. Si `highlight` es True, se aplica un color de resaltado,
        y si es False, se aplica un color de fondo neutro.
        """
        color = QColor(255, 171, 145) if highlight else QColor(255, 243, 224)
        for row in range(self.rowCount()):
            self.item(row, column_index).setBackground(color)
