from PyQt5.QtWidgets import (
QDialog, QDialogButtonBox, QLineEdit, QFormLayout, QMessageBox, QFileDialog)
import PyQt5.QtCore as QtCore

class InputDialog(QDialog):
    def __init__(self, labels: list[str], title: str = 'default title' , stylesheet: str = None, parent = None):
        super().__init__(parent,  QtCore.Qt.WindowCloseButtonHint)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout = QFormLayout(self)
        self.setWindowTitle(title)
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QFormLayout
from PyQt5.QtCore import Qt, pyqtSlot

class InputDialog(QDialog):
    def __init__(self, labels: list[str], title: str = 'default title', stylesheet: str = None, parent=None):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)
        
        # Configuración del botón de Aceptar y Cancelar
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        
        layout = QFormLayout(self)
        self.setWindowTitle(title)

        # Si hay una hoja de estilo personalizada, aplicarla
        if stylesheet:
            self.setStyleSheet(stylesheet)
        else:
            # Aplicar estilo por defecto para el fondo y el texto
            self.setStyleSheet("""
                QDialog {
                    background-color: black;
                    color: white;
                }
                QLabel {
                    color: white;
                }
                QLineEdit {
                    background-color: black;
                    color: white;
                    border: 1px solid white;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)

        self.inputs = []
        for lab in labels:
            line_edit = QLineEdit(self)
            self.inputs.append(line_edit)
            layout.addRow(lab, line_edit)

        layout.addWidget(buttonBox)

        # Conectar los botones
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def get_inputs(self):
        return tuple(input.text() for input in self.inputs)

def show_message(message: str, parent = None) -> None:
    """
    Shows a message in a pop up window

    Parameters 
    -----------
    message : str
        String to show in the pop up

    Returns
    -----------
        None
    """
    msg_box = QMessageBox(parent = parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle("Éxito")
    msg_box.exec_()

def show_error(message: str, parent = None) -> None:
    """
    Shows an error message in a pop up window

    Parameters 
    -----------
    message : str
        Error string to show in the pop up

    Returns
    -----------
        None
    """
    error_msg = QMessageBox(parent = parent)
    error_msg.setIcon(QMessageBox.Critical)
    error_msg.setText(message)
    error_msg.setWindowTitle('Error')
    error_msg.exec_()

def open_file_dialog(parent = None) -> None:
    """
    Shows the dialog to open files and returns the selected directory

    Returns
    -----------
        file_path: str
    """
    options = QFileDialog.Options()
    res = 'Todos los Archivos (*.*);;Archivos CSV (*.csv);;Archivos Excel'
    res += ' (*.xlsx *.xls);;Base de datos SQLite (*.sqlite *.db)'
    file_path, _ = QFileDialog.getOpenFileName(parent, 'Seleccionar archivo',
        '', res, options = options)
    return file_path

def save_file_dialog(parent = None) -> None:
    """
    Shows the dialog to save files and returns the selected directory

    Returns
    -----------
        file_path: str
    """
    options = QFileDialog.Options()
    res = 'Archivo joblib (*.joblib)'
    file_path, _ = QFileDialog.getSaveFileName(parent, 'Guardar archivo',
        '', res, options = options)
    return file_path

