from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QTabBar
import pandas as pd

from tabs.data_tab import DataTab
from tabs.lineal_model_tab import LinealModelTab

class MainWindow(QTabWidget):
    """
    Ventana principal de la aplicación que gestiona las pestañas.
    """

    def __init__(self):
        """
        Inicializa la ventana principal y configura sus propiedades.
        """
        super().__init__()

        # Set main window title and geometry
        self.setWindowTitle('Linear Regression Model Maker')
        self.setGeometry(100, 100, 1200, 800)

        # Load stylesheet
        stylesheet_doc = 'src/assets/stylesheet.txt'
        with open(stylesheet_doc) as stylesheet_doc:
            self.setStyleSheet(stylesheet_doc.read())

        # Enable close button on all tabs initially
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        # Initialize tabs
        self.init_tabs()

    def init_tabs(self):
        """
        Inicializa las pestañas de la ventana principal.
        """
        # Crear la pestaña de datos
        self.data_tab = DataTab()

        # Agregar la pestaña de datos al QTabWidget
        self.addTab(self.data_tab, "Datos")

        # Desactivar el botón de cerrar solo en la pestaña "Datos" (índice 0)
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # Conectar la carga de datos para crear el modelo lineal después
        self.tabs_counter = 0
        self.data_tab.column_selector.confirm_button.clicked.connect(self.create_linear_model_tab)

    def create_linear_model_tab(self):
        """
        Crea la pestaña de modelo lineal si los datos están disponibles.
        """
        self.tabs_counter += 1
        # Crear la pestaña de modelo lineal
        self.linear_model_tab = LinealModelTab(self.data_tab.data, 
                                               self.data_tab.selected_input_columns, 
                                               self.data_tab.selected_output_column)

        # Agregar la pestaña de modelo lineal con la "X" de cierre
        self.addTab(self.linear_model_tab, f"Modelo {self.tabs_counter}")

    def close_tab(self, index):
        """
        Cierra la pestaña en el índice dado.
        """
        # Evita que la pestaña de datos se cierre
        if index != 0:  # Asumiendo que la pestaña de datos es la primera pestaña
            self.removeTab(index)