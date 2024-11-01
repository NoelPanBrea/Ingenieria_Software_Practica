from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel

from tabs.data_tab import DataTab

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

        Crea la pestaña de datos y una pestaña vacía. Luego, agrega estas
        pestañas al QTabWidget para que el usuario pueda navegar entre ellas.
        """
        # Create the first tab (data tab)
        self.data_tab = DataTab()
        
        # Create the second tab (empty for now)
        self.empty_tab = QWidget()
        empty_layout = QVBoxLayout()
        empty_label = QLabel("Esta pestaña está vacía de momento.")
        empty_layout.addWidget(empty_label)
        self.empty_tab.setLayout(empty_layout)

        # Add tabs to the QTabWidget
        self.addTab(self.data_tab, "Data")
        self.addTab(self.empty_tab, "Empty")
