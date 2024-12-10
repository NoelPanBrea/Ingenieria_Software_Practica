from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QApplication, QTabBar, QHBoxLayout, QToolButton, QMenu, QMessageBox)
from PyQt5.QtCore import Qt
from tabs.data_tab import DataTab
from tabs.linear_model_tab import LinearModelTab
from ui.popup_handler import show_error

class MainWindow(QMainWindow):
    """
    Main window of the application that manages tabs and their interactions.

    This window contains a central `QTabWidget` where different tabs for data
    loading, linear model creation, and other operations are managed.

    Attributes
    ----------
    central_widget : QWidget
        The main widget for the window.
    main_layout : QVBoxLayout
        The layout that organizes the main components.
    tab_widget : QTabWidget
        The widget containing all the tabs.
    settings_button : QToolButton
        Button for accessing theme settings.
    style_menu : QMenu
        Menu containing theme options.
    style_sheets : dict
        Dictionary mapping style names to their file paths.
    data_tab : DataTab
        The default tab for loading and managing data.
    tabs_counter : int
        Counter for the number of `LinearModelTab` instances.
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
        
        # Add actions for each theme to the menu
        for style_name in self.style_sheets.keys():
            action = self.style_menu.addAction(style_name)
            action.setObjectName("menuItem")  # Agregamos un nombre de objeto para los items
            action.triggered.connect(
                lambda checked, name=style_name: self.load_style(self.style_sheets[name]))
        
        # Attach the menu to the settings button
        self.settings_button.setMenu(self.style_menu)
        self.settings_button.setPopupMode(QToolButton.InstantPopup)

        # Create info button
        self.info_button = QToolButton()
        self.info_button.setText("ℹ")
        self.info_button.setFixedSize(50, 50) 
        self.info_button.clicked.connect(self.show_info)
        
        # Create tab corner widget for left side
        corner_widget = QWidget()
        corner_layout = QHBoxLayout(corner_widget)
        corner_layout.setContentsMargins(10, 0, 10, 0)
        corner_layout.addWidget(self.info_button)
        corner_layout.addWidget(self.settings_button)
        
        # Set corner widget in tab widget
        self.tab_widget.setCornerWidget(corner_widget, Qt.TopLeftCorner)

        # Load initial style
        self.load_style(self.style_sheets["Tema Rosa Oscuro"])

    def show_info(self):
        """
        Displays an information dialog explaining how the application works.
        """
        info_message = QMessageBox(self)
        info_message.setWindowTitle("Información")
        info_message.setText(
            "Bienvenido a la aplicación Linear Regression Model Maker.\n\n"
            "1. En la pestaña principal, puedes cargar un archivo CSV o cargar un modelo ya creado.\n"
            "2. Para crear un modelo escoga las columnas de entrada y la columna de salida que desee y confirme la selección.\n"
            "3. Si hay datos nulos será necesario preprocesarlos con las opciones disponibles que aparecerán.\n"	
            "4. Cambie a la pestaña del modleo para poder entrenar el modelo.\n"
            "5. En esta pestaña podrá cambiar la descripción, interactuar con la gráfica y realizar predicciones sobre el modelo.\n"
            "6. Si desea guardar el modelo entrenado o la gráfica de este podrá hacerlo en la pestaña del modelo.\n"
            "7. Explora múltiples modelos abriendo nuevas pestañas o cargando modelos ya creados.\n\n"
            "¡Disfruta creando modelos lineales de manera sencilla!"
        )
        info_message.setIcon(QMessageBox.Information)
        info_message.setStandardButtons(QMessageBox.Ok)
        info_message.exec_()
        
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

        # Create the initial data tab
        self.data_tab = DataTab()
        self.tab_widget.addTab(self.data_tab, "Datos")

        # Disable the close button for the first tab
        self.tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # Connect events for creating or loading a linear model
        self.tabs_counter = 0
        self.data_tab.column_selector.confirm_button.clicked.connect(self.create_linear_model_tab)
        self.data_tab.model_button.clicked.connect(self.load_model_open_tab)

    def create_linear_model_tab(self):
        """
        Creates the linear model tab if the data is available.
        """

        # Check if input_columns or output_column is None
        if not self.data_tab.selected_input_columns or not self.data_tab.selected_output_column:
            show_error("Debe seleccionar columnas de entrada y salida antes de crear un modelo.", self)
            return

        # Check for null values in selected columns
        selected_columns = self.data_tab.selected_input_columns + [self.data_tab.selected_output_column]
        has_nulls = self.data_tab.data[selected_columns].isnull().any().any()
        
        if has_nulls:
            show_error("Hay valores nulos en los datos seleccionados. Por favor, aplique algún método de preprocesado antes de crear el modelo.", self)
            return

        self.tabs_counter += 1

        # Create a new linear model tab
        LinearModelTab(
            data=self.data_tab.data, 
            input_columns=self.data_tab.selected_input_columns, 
            output_column=self.data_tab.selected_output_column,
            loaded_model=None)

        # Clear the description of the newly created tab
        LinearModelTab.tab_list[-1].model_description.clear_description()
        
        # Add the new tab to the tab widget
        self.tab_widget.addTab(LinearModelTab.tab_list[-1],
                     f"Modelo {self.tabs_counter}")
        
        # Close any old tabs with untrained models
        if len(LinearModelTab.tab_list) > 1 and\
              LinearModelTab.tab_list[-2].model is None:
            self.close_tab(len(LinearModelTab.tab_list) - 1)

    def load_model_open_tab(self) -> bool:
        """    
        Loads a model and opens a LinearModelTab.
        """
        model_data = self.data_tab.load_model()
        if model_data:
            try:
                # Increment tab counter
                self.tabs_counter += 1
                new_tab = LinearModelTab(loaded_model=model_data)
                # Add the new tab and switch to it
                tab_index = self.tab_widget.addTab(new_tab, f"Modelo {self.tabs_counter}")
                self.tab_widget.setCurrentIndex(tab_index)                
                # Force UI update
                self.tab_widget.update()
                QApplication.processEvents()
                return True
                
            except Exception as e:
                show_error(f"Error al crear la pestaña del modelo: {str(e)}", self)
                return False
        
        return False
    
    def close_tab(self, index: int):
        """
        Closes the tab at the given index.

        Parameters
        ----------
        index : int
            Index of the tab to close.
        """
        # Prevent closing the first tab (data tab)
        if index != 0:
            self.tab_widget.removeTab(index)
            del(LinearModelTab.tab_list[index - 1])
    
    def resizeEvent(self, event):
        """
        Handles window resize events to adjust the data tab layout.

        Parameters
        ----------
        event : QResizeEvent
            The resize event triggered when the window is resized.
        """
        QMainWindow.resizeEvent(self, event)
        if hasattr(self, 'data_tab') and self.data_tab.data is not None:
            self.data_tab.table.fill_area(self.data_tab.data.shape[1])