from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class PreprocessToolbar(QWidget):
    """
    Preprocessing toolbar that allows selection of various data preprocessing methods.

    This toolbar contains buttons representing preprocessing methods (delete nulls,
    mean, median, constants) and an apply button.

    Parameters
    ----------
    parent : QWidget, optional
        The main widget that will contain the preprocessing toolbar, by default None.

    Attributes
    ----------
    buttons : dict
        Dictionary storing the buttons for preprocessing methods.
    apply_button : QPushButton
        Button to apply the selected preprocessing method.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.on_method_selected = None

    def init_ui(self):
        """
        Initializes and arranges the preprocessing buttons in a horizontal toolbar.

        Notes
        -----
        All buttons are initially hidden and are only shown when the user has selected
        the appropriate columns for preprocessing.
        """
        layout = QHBoxLayout()
        self.buttons = {}

        button_configs = [
            ('delete', 'Eliminar'),
            ('mean', 'Media'),
            ('median', 'Mediana'),
            ('constant', 'Constantes'),
        ]

        for method, label in button_configs:
            button = QPushButton(label)
            button.hide()
            self.buttons[method] = button
            layout.addWidget(button)

            button.clicked.connect(
                lambda _, method=method: self.handle_button_click(method))

        self.setLayout(layout)

    def handle_button_click(self, method):
        """
        Handles the click event of a preprocessing method button.

        Parameters
        ----------
        method : str
            The name of the preprocessing method to apply.

        Notes
        -----
        This method invokes the callback `on_method_selected` if it is set.
        """
        if self.on_method_selected:
            self.on_method_selected(method)

    def show_buttons(self):
        """
        Displays all preprocessing method buttons
        """
        for button in self.buttons.values():
            button.show()

    def hide_buttons(self):
        """
        Hides all preprocessing method buttons
        """
        for button in self.buttons.values():
            button.hide()
