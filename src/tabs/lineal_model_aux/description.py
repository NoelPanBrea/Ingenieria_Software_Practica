import os
from PyQt5.QtWidgets import (QLabel, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt

class ModelDescription:
    DEFAULT_TEXT = "Haz clic para añadir una descripción..."
    
    def __init__(self, parent_widget=None):
        self.parent_widget = parent_widget
        self.description = ""
        self.setup_ui_elements()
        self.setup_events()

    def setup_ui_elements(self):
        """
        Configura los elementos de la UI relacionados con la descripción
        """
        self.display_label = QLabel(self.DEFAULT_TEXT)
        self.display_label.setStyleSheet("""
            QLabel {
                color: #4E342E;
                font-size: 15px;
                padding: 2px;
            }
        """)
        self.display_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.display_label.setMouseTracking(True)
        self.display_label.setCursor(Qt.PointingHandCursor)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe aquí la descripción del modelo...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                font-size: 11px;
                padding: 2px;
            }
        """)
        self.input_field.hide()

    def setup_events(self):
        """Configura los eventos de los widgets"""
        self.input_field.returnPressed.connect(
            lambda: self.update_description())
        self.input_field.focusOutEvent = self.on_focus_lost
        self.display_label.mousePressEvent = self.on_label_click

    def show_edit_mode(self):
        current_text = self.display_label.text()
        self.display_label.hide()
        
        if current_text == self.DEFAULT_TEXT:
            self.input_field.setText("")
        else:
            self.input_field.setText(current_text)
            
        self.input_field.show()
        self.input_field.setFocus()

    def update_description(self):
        description = self.input_field.text()
        
        if not description:
            self.display_label.setText(self.DEFAULT_TEXT)
        else:
            self.description = description
            self.display_label.setText(description)
        
        self.input_field.hide()
        self.display_label.show()

    def on_label_click(self, event):
        """Maneja el clic en la etiqueta de descripción"""
        self.show_edit_mode()

    def on_focus_lost(self, event):
        """Maneja la pérdida de foco del campo de entrada"""
        self.update_description()
        QLineEdit.focusOutEvent(self.input_field, event)

    def add_to_layout(self, layout):
        """Añade los widgets al layout proporcionado"""
        layout.addWidget(self.display_label)
        layout.addWidget(self.input_field)

    def clear_description(self):
        """Limpia la descripción"""
        self.description = ""
        self.display_label.setText(self.DEFAULT_TEXT)

    def get_description(self):
        """Obtiene la descripción actual"""
        if self.display_label.text() == self.DEFAULT_TEXT:
            return ""
        return self.description

    def set_description(self, description):
        """Establece una descripción cargada"""
        if description:
            self.description = description
            self.display_label.setText(description)
        else:
            self.clear_description()