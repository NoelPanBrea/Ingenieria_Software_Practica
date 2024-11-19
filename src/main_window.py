from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QTabBar
import pandas as pd
from PyQt5 import QtCore
from tabs.data_tab import DataTab
from tabs.lineal_model_tab import LinealModelTab

class MainWindow(QTabWidget):
    """
    Main window of the application that manages the tabs.
    """

    def __init__(self):
        """
        Initializes the main window and sets its properties.
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

    def resizeEvent(self, event):
        QTabWidget.resizeEvent(self, event)
        if hasattr(self, 'data_tab'):
            self.data_tab.column_selector.input_column_selector.setFixedWidth(self.width() // 2 - 25)
            if self.data_tab.data is not None:
                w = 0
                for i in range(self.data_tab.data.shape[1]):
                    w += self.data_tab.table.columnWidth(i)
                if w < self.width():
                    for i in range(self.data_tab.data.shape[1]):
                        self.data_tab.table.setColumnWidth(i, self.width() // self.data_tab.data.shape[1])


    def closeEvent(self, event):
        #TODO Aquí podríamos añadir una ventana que recuerde al usuario que tiene modelos sin guardar 
        event.accept()


    def init_tabs(self):
        """
        Initializes the tabs of the main window.
        """
        # Crear la pestaña de datos
        self.data_tab = DataTab()

        # Agregar la pestaña de datos al QTabWidget
        self.addTab(self.data_tab, "Datos")

        # Desactivar el botón de cerrar solo en la pestaña "Datos" (índice 0)
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # Conectar la carga de datos para crear el modelo lineal después
        self.tabs_counter = 0
        self.linear_model_tab_list = []
        self.data_tab.column_selector.confirm_button.clicked.connect(self.create_linear_model_tab)

        #Crear pestana al cargar modelo
        #self.data_tab.model_button.clicked.connect(self.load_model_open_tab)
    def create_linear_model_tab(self):
        """
        Creates the linear model tab if the data is available.
        """

        self.tabs_counter += 1
        # Crear la pestaña de modelo lineal
        self.linear_model_tab_list.append(LinealModelTab(self.data_tab.data, 
                                        self.data_tab.selected_input_columns, 
                                    self.data_tab.selected_output_column))

        # Limpiar la descripción al crear una nueva pestaña
        self.linear_model_tab_list[-1].model_description.clear_description()
        
        # Agregar la pestaña de modelo lineal con la "X" de cierre
        self.addTab(self.linear_model_tab_list[-1],
                     f"Modelo {self.tabs_counter}")
        if len(self.linear_model_tab_list) > 1 and\
              self.linear_model_tab_list[-2].model is None:
            self.close_tab(len(self.linear_model_tab_list) - 1)


    def load_model_open_tab(self):
        """    
        Loads a model and opens a LinealModelTab.
        """
        model_loaded = self.data_tab.load_model()
        if model_loaded:
            self.create_linear_model_tab() #Abrir pestaña de modelo lineal
        
    def close_tab(self, index):
        """
        Closes the tab at the given index.
        """
        # Evita que la pestaña de datos se cierre
        if index != 0:  # Asumiendo que la pestaña de datos es la primera pestaña
            self.removeTab(index)
            del(self.linear_model_tab_list[index - 1])
