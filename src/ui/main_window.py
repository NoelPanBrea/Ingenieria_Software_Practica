from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QTabBar, QHBoxLayout, QToolButton, QMenu)
from PyQt5.QtCore import Qt
from tabs.data_tab import DataTab
from tabs.lineal_model_tab import LinealModelTab

class MainWindow(QMainWindow):
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

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Create tab widget first
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tab_widget)

        # Load stylesheet
        self.init_styles()

        # Initialize tabs
        self.init_tabs()

    def init_styles(self):
        """
        Initialize the style system and selector.
        """
        # Define available styles
        self.style_sheets = {
            "Tema Rosa Oscuro": "src/assets/stylesheet_pink.txt",
            "Tema Rosa Claro": "src/assets/stylesheet_light_pink.txt",
            "Tema Verde": "src/assets/stylesheet_green.txt",
            "Tema Azul": "src/assets/stylesheet_blue.txt"
        }

        # Create settings button
        self.settings_button = QToolButton()
        self.settings_button.setText("⚙")
        self.settings_button.setFixedSize(50, 50)  # Aseguramos que es cuadrado
        
        # Create menu for the button
        self.style_menu = QMenu(self.settings_button)
        self.style_menu.setObjectName("settingsMenu") # Agregamos un nombre de objeto para poder estilizarlo
        
        # Crear las acciones del menú con un estilo específico
        for style_name in self.style_sheets.keys():
            action = self.style_menu.addAction(style_name)
            action.setObjectName("menuItem")  # Agregamos un nombre de objeto para los items
            action.triggered.connect(
                lambda checked, name=style_name: self.load_style(self.style_sheets[name]))
        
        self.settings_button.setMenu(self.style_menu)
        self.settings_button.setPopupMode(QToolButton.InstantPopup)

        # Create tab corner widget for left side
        corner_widget = QWidget()
        corner_layout = QHBoxLayout(corner_widget)
        corner_layout.setContentsMargins(10, 0, 10, 0)
        corner_layout.addWidget(self.settings_button)
        
        # Set corner widget in tab widget
        self.tab_widget.setCornerWidget(corner_widget, Qt.TopLeftCorner)

        # Load initial style
        self.load_style(self.style_sheets["Tema Rosa Oscuro"])

    def load_style(self, style_path):
        """
        Load a style sheet from a file.

        Parameters
        ----------
        style_path : str
            Path to the style sheet file
        """
        try:
            with open(style_path, 'r', encoding='utf-8') as stylesheet_doc:
                self.setStyleSheet(stylesheet_doc.read())
        except Exception as e:
            print(f"Error loading style: {e}")

    def init_tabs(self):
        """
        Initializes the tabs of the main window.
        """
        self.data_tab = DataTab()

        self.tab_widget.addTab(self.data_tab, "Datos")

        # Desactivar el botón de cerrar solo en la pestaña "Datos" (índice 0)
        self.tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # Conectar la carga de datos para crear el modelo lineal después
        self.tabs_counter = 0
        self.data_tab.column_selector.confirm_button.clicked.connect(self.create_linear_model_tab)

    def create_linear_model_tab(self):
        """
        Creates the linear model tab if the data is available.
        """

        self.tabs_counter += 1
        # Crear la pestaña de modelo lineal
        LinealModelTab(self.data_tab.data,
             self.data_tab.selected_input_columns,
             self.data_tab.selected_output_column)

        # Limpiar la descripción al crear una nueva pestaña
        LinealModelTab.tab_list[-1].model_description.clear_description()
        
        # Agregar la pestaña de modelo lineal con la "X" de cierre
        self.tab_widget.addTab(LinealModelTab.tab_list[-1],
                     f"Modelo {self.tabs_counter}")
        if len(LinealModelTab.tab_list) > 1 and\
              LinealModelTab.tab_list[-2].model is None:
            self.close_tab(len(LinealModelTab.tab_list) - 1)

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
            self.tab_widget.removeTab(index)
            del(LinealModelTab.tab_list[index - 1])
    
    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        if hasattr(self, 'data_tab') and self.data_tab.data is not None:
            self.data_tab.table.fill_area(self.data_tab.data.shape[1])