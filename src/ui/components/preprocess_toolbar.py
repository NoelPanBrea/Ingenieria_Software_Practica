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

        self.apply_button = QPushButton('Aplicar preprocesado')
        self.apply_button.hide()
        self.apply_button.setMinimumWidth(400)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def show_buttons(self):
        """
        Displays all preprocessing method buttons and the apply button.
        """
        for button in self.buttons.values():
            button.show()
        self.apply_button.show()
    
    def hide_buttons(self):
        """
        Hides all preprocessing method buttons and the apply button.
        """
        for button in self.buttons.values():
            button.hide()
        self.apply_button.hide()
