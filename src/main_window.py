from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel
import pandas as pd

from tabs.data_tab import DataTab
from tabs.linear_model_tab import LinearModelTab

class MainWindow(QTabWidget):
    """
    Ventana principal de la aplicación que gestiona las pestañas.

    Esta clase extiende QTabWidget para proporcionar una interfaz de usuario que
    permite navegar entre diferentes pestañas. En esta implementación, incluye
    una pestaña para gestionar datos y una pestaña vacía.

    Important Attributes
    --------------------
    data_tab : DataTab
        Instancia de la pestaña de datos que permite al usuario cargar y preprocesar
        conjuntos de datos.
    empty_tab : QWidget
        Pestaña vacía que puede ser utilizada para futuras funcionalidades.
    
    Other Attributes
    ----------------
    title : str
        Título de la ventana principal.
    geometry : tuple
        Geometría de la ventana principal (x, y, ancho, alto).
    stylesheet_doc : str
        Ruta al archivo de la hoja de estilos de la aplicación.
    """

    def __init__(self):
        """
        Inicializa la ventana principal y configura sus propiedades.

        Se establece el título y la geometría de la ventana, así como la
        hoja de estilos a partir de un archivo externo. Luego, se inicializan
        las pestañas de la aplicación.
        """
        super().__init__()

        # Set main window title and geometry
        self.setWindowTitle('Linear Regression Model Maker')
        self.setGeometry(100, 100, 1200, 800)

        # Load stylesheet
        stylesheet_doc = 'src/assets/stylesheet.txt'
        with open(stylesheet_doc) as stylesheet_doc:
            self.setStyleSheet(stylesheet_doc.read())

        # Initialize tabs
        self.init_tabs()

    def init_tabs(self):
        """
        Inicializa las pestañas de la ventana principal.

        Crea la pestaña de datos y la pestaña de modelo lineal (si hay datos),
        luego agrega estas pestañas al QTabWidget.
        """
        # Crear la pestaña de datos
        self.data_tab = DataTab()

        # Conectar la carga de datos para crear el modelo lineal después
        self.data_tab.load_button.clicked.connect(self.create_linear_model_tab)

        # Agregar la pestaña de datos al QTabWidget
        self.addTab(self.data_tab, "Datos")

    def create_linear_model_tab(self):
        """
        Crea la pestaña de modelo lineal si los datos están disponibles.
        """
        if self.data_tab.data is not None:
            input_columns = ['latitude', 'longitude']  # Ajusta según tus datos
            output_column = 'population'  # Ajusta según tus datos

            # Crear la pestaña de modelo lineal
            self.linear_model_tab = LinearModelTab(self.data_tab.data, input_columns, output_column)

            # Verificar si ya existe una pestaña de modelo lineal y reemplazarla si es necesario
            index = self.indexOf(self.linear_model_tab) if hasattr(self, 'linear_model_tab') else -1
            if index == -1:
                # Agregar la pestaña si no existe
                self.addTab(self.linear_model_tab, "Modelo Lineal")
            else:
                # Reemplazar la pestaña existente
                self.removeTab(index)
                self.addTab(self.linear_model_tab, "Modelo Lineal")
        else:
            print("Por favor, carga los datos antes de crear el modelo lineal.")
