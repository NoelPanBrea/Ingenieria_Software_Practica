from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout

class PreprocessToolbar(QWidget):
    """
    Barra de herramientas de preprocesado que permite seleccionar diferentes métodos
    de preprocesado de datos.

    Esta barra contiene botones que representan métodos de preprocesado (eliminar nulos,
    media, mediana, constantes) y un botón de aplicación.

    Parameters
    ----------
    parent : QWidget, optional
        El widget principal que contendrá la barra de herramientas de preprocesado, por defecto None.

    Attributes
    ----------
    buttons : dict
        Diccionario que almacena los botones de métodos de preprocesado.
    apply_button : QPushButton
        Botón para aplicar el preprocesado seleccionado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Inicializa y organiza los botones de preprocesado en una barra horizontal.

        Notes
        -----
        Todos los botones se ocultan inicialmente y solo se muestran cuando el usuario ha seleccionado
        las columnas adecuadas para el preprocesado.
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
        Muestra todos los botones de métodos de preprocesado y el botón de aplicar.
        """
        for button in self.buttons.values():
            button.show()
        self.apply_button.show()
