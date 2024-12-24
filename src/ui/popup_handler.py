from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QLineEdit, QFormLayout, QMessageBox, QFileDialog)
from PyQt5 import QtCore


class InputDialog(QDialog):
    """
    A dialog window for collecting user input.

    This dialog displays a set of input fields (QLineEdit) associated with given labels. 
    It includes "OK" and "Cancel" buttons to confirm or reject the input.

    Attributes
    ----------
    inputs : list[QLineEdit]
        List of input fields for user entry.
    """

    def __init__(self, labels: list[str], title: str = "default title",
                 stylesheet: str = None, parent=None):

        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Create "Aceptar" and "Cancelar" buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        # Set up the dialog layout
        layout = QFormLayout(self)
        self.setWindowTitle(title)

        # Apply a custom stylesheet if provided
        if stylesheet:
            self.setStyleSheet(stylesheet)

        # Initialize input fields
        self.inputs = []
        for lab in labels:
            # Create a QLineEdit for each label and add it to the layout
            line_edit = QLineEdit(self)
            self.inputs.append(line_edit)
            layout.addRow(lab, line_edit)

        # Add the button box to the layout
        layout.addWidget(self.buttonBox)

        # Connect the buttons to their respective methods
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_inputs(self) -> tuple[str]:
        """
        Retrieves the user inputs from all input fields.

        Returns
        -------
        tuple[str]
            A tuple containing the text entered in each input field.
        """
        return tuple(input.text() for input in self.inputs)


def show_message(message: str, parent=None):
    """
    Shows a message in a pop up window

    Parameters 
    -----------
    message : str
        String to show in the pop up
    """
    msg_box = QMessageBox(parent=parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle("Éxito")
    msg_box.exec_()


def show_warning(message: str, parent=None):
    """
    Shows an error message in a pop up window

    Parameters 
    -----------
    message : str
        Error string to show in the pop up
    """
    error_msg = QMessageBox(parent=parent)
    error_msg.setIcon(QMessageBox.Warning)
    error_msg.setText(message)
    error_msg.setWindowTitle("Atención")
    error_msg.exec_()


def show_error(message: str, parent=None):
    """
    Shows an error message in a pop up window

    Parameters 
    -----------
    message : str
        Error string to show in the pop up
    """
    error_msg = QMessageBox(parent=parent)
    error_msg.setIcon(QMessageBox.Critical)
    error_msg.setText(message)
    error_msg.setWindowTitle("Error")
    error_msg.exec_()


def show_suggestion(title: str, text: str, informative_text: str, parent=None):
    msg_box = QMessageBox(parent=parent)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setInformativeText(informative_text)
    msg_box.setWindowTitle("Recomendación")
    msg_box.setText("El modelo no tiene una descripción.")
    msg_box.setInformativeText(
        "Se recomienda añadir una descripción para mejor documentación. ¿Desea continuar sin descripción?")

    # Create custom button
    msg_box.addButton("Sí", QMessageBox.YesRole)
    no_button = msg_box.addButton("No", QMessageBox.NoRole)
    msg_box.setDefaultButton(no_button)

    msg_box.exec_()
    return msg_box.clickedButton() == no_button


def open_file_dialog(parent=None) -> str:
    """
    Shows the dialog to open files and returns the selected directory

    Returns
    -----------
        file_path: str
    """
    options = QFileDialog.Options()
    res = "Todos los Archivos (*.*);;Archivos CSV (*.csv);;Archivos Excel"
    res += " (*.xlsx *.xls);;Base de datos SQLite (*.sqlite *.db)"
    file_path, _ = QFileDialog.getOpenFileName(parent, "Seleccionar archivo",
                                               "", res, options=options)
    return file_path


def save_file_dialog(parent=None) -> str:
    """
    Shows the dialog to save files and returns the selected directory

    Returns
    -----------
        file_path: str
    """
    options = QFileDialog.Options()
    res = "Archivo joblib (*.joblib)"
    file_path, _ = QFileDialog.getSaveFileName(parent, "Guardar archivo",
                                               "", res, options=options)
    return file_path


def open_model_dialog(parent=None) -> str:
    """
    Shows the dialog to load models
    """
    options = QFileDialog.Options()
    res = "Todos los Archivos (*.*);;Archivos JOBLIB (*.joblib)"
    file_path, _ = QFileDialog.getOpenFileName(parent, "Seleccionar archivo",
                                               "", res, options=options)
    return file_path
