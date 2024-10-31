from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, 
                            QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt

from .model_description_storage import ModelDescription

class LinealModelTab(QWidget):
    """
    Crea la pestaña para el modelo lineal
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_description = ModelDescription()
        self.setup_ui()
        
    def setup_ui(self):
        """
        Configura la pestaña del modelo lineal
        """
        layout = QVBoxLayout()

        # Configurar etiqueta para mostrar la descripción
        self.description_display = QLabel("Haz clic para añadir una descripción...")
        self.description_display.setStyleSheet("""
            QLabel {
                color: #4E342E;
                font-size: 15px;
                padding: 2px;
            }
        """)
        self.description_display.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.description_display.setMouseTracking(True)
        self.description_display.setCursor(Qt.PointingHandCursor)
        
        # Configurar campo de texto editable
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Escribe aquí la descripción del modelo...")
        self.description_input.setStyleSheet("""
            QLineEdit {
                font-size: 11px;
                padding: 2px;
            }
        """)
        self.description_input.hide()

        # Conectar eventos de interacción
        self.description_input.returnPressed.connect(self.save_description)
        self.description_input.focusOutEvent = self.on_focus_lost
        self.description_display.mousePressEvent = self.on_label_click

        # Cargar descripción desde la base de datos o archivo
        loaded_description = self.model_description.load_description()
        if loaded_description:
            self.description_display.setText(loaded_description)
        
        layout.addWidget(self.description_display)
        layout.addWidget(self.description_input)
        
        # Espaciador para empujar widgets hacia arriba
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        self.setLayout(layout)

    def on_label_click(self, event):
        """
        Activa el modo de edición cuando se hace clic en la descripción.
        """
        self.description_display.hide()
        current_text = self.description_display.text()
        
        # Limpiar el campo si tiene el texto por defecto
        if current_text == "Haz clic para añadir una descripción...":
            self.description_input.setText("")
        else:
            self.description_input.setText(current_text)
            
        self.description_input.show()
        self.description_input.setFocus()

    def on_focus_lost(self, event):
        """
        Guarda la descripción cuando el campo de texto pierde el foco.
        """
        self.save_description()
        QLineEdit.focusOutEvent(self.description_input, event)

    def save_description(self):
        """
        Guarda la descripción y vuelve al modo de visualización.
        """
        description = self.description_input.text()
        
        if not description:
            self.description_display.setText("Haz clic para añadir una descripción...")
        else:
            self.description_display.setText(description)
            self.model_description.save_description(description)  # Guardar en almacenamiento
        
        self.description_input.hide()
        self.description_display.show()

    # Método para obtener la descripción actual
    def get_current_description(self):
        """
        Retorna la descripción actual del modelo.
        """
        text = self.description_display.text()
        if text == "(Opcional) Haz clic para añadir una descripción...":
            return ""
        return text

    # Método para establecer una descripción 
    def set_description(self, description):
        """
        Establece una descripción.
        """
        if description:
            self.description_display.setText(description)
            self.model_description.save_description(description)
