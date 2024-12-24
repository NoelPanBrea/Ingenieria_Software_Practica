from PyQt5.QtWidgets import (QLabel, QLineEdit)
from PyQt5.QtCore import Qt


class ModelDescription:
    """
    Manages the user interface and functionality for a model's description.

    This class provides an editable description field, switching between a label
    and an input field, along with methods to retrieve, update, or clear the description.

    Attributes
    ----------
    DEFAULT_TEXT : str
        Default placeholder text when no description is set.
    parent_widget : QWidget, optional
        The parent widget for the description elements.
    description : str
        The current description of the model.
    display_label : QLabel
        Label used to display the description.
    input_field : QLineEdit
        Input field used to edit the description.
    """
    DEFAULT_TEXT = "Haz clic para añadir una descripción..."

    def __init__(self, parent_widget=None):
        """
        Initializes the ModelDescription object.

        Parameters
        ----------
        parent_widget : QWidget, optional
            The parent widget for the description elements. Defaults to None.
        """
        self.parent_widget = parent_widget
        self.description = ""
        self.setup_ui_elements()
        self.setup_events()

    def setup_ui_elements(self):
        """
        Sets up the UI elements related to the description.
        """

        # Create the display label
        self.display_label = QLabel(self.DEFAULT_TEXT)
        self.display_label.setObjectName("displayLabel")
        self.display_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.display_label.setMouseTracking(True)
        self.display_label.setCursor(Qt.PointingHandCursor)

        # Create the input field for editing the description
        self.input_field = QLineEdit()
        self.input_field.setObjectName("modelInput")
        self.input_field.setPlaceholderText(
            "Escribe aquí la descripción del modelo...")
        self.input_field.hide()

    def setup_events(self):
        """
        Sets up the events for the widgets.
        """
        self.input_field.returnPressed.connect(
            lambda: self.update_description())
        self.input_field.focusOutEvent = self.on_focus_lost
        self.display_label.mousePressEvent = self.on_label_click

    def show_edit_mode(self):
        """
        Enables the edit mode, showing the input field and hiding the label.

        If the current label text is the default placeholder text,
        the input field will be empty. Otherwise, it will contain the label's text.
        """
        current_text = self.display_label.text()
        self.display_label.hide()

        # Set input field text based on the current label content
        if current_text == self.DEFAULT_TEXT:
            self.input_field.setText("")
        else:
            self.input_field.setText(current_text)

        self.input_field.show()
        self.input_field.setFocus()

    def update_description(self):
        """
        Updates the description based on the input field's content.

        If the input field is empty, the default placeholder text is set.
        Otherwise, the description is updated with the input text.
        """
        description = self.input_field.text()

        if not description:
            # Set default placeholder text if the input is empty
            self.display_label.setText(self.DEFAULT_TEXT)
        else:
            # Update the description and label text
            self.description = description
            self.display_label.setText(description)

        self.input_field.hide()
        self.display_label.show()

    def on_label_click(self, event):
        """
        Handles the click on the description label.
        """
        self.show_edit_mode()

    def on_focus_lost(self, event):
        """
        Handles the loss of focus from the input field.
        """
        self.update_description()
        QLineEdit.focusOutEvent(self.input_field, event)

    def add_to_layout(self, layout):
        """
        Adds the widgets to the provided layout.
        """
        layout.addWidget(self.display_label)
        layout.addWidget(self.input_field)

    def clear_description(self):
        """
        Clears the description.
        """
        self.description = ""
        self.display_label.setText(self.DEFAULT_TEXT)

    def get_description(self):
        """
        Gets the current description.
        """
        if self.display_label.text() == self.DEFAULT_TEXT:
            return ""
        return self.description

    def set_description(self, description):
        """
        Sets a loaded description.
        """
        if description:
            self.description = description
            self.display_label.setText(description)
        else:
            self.clear_description()
