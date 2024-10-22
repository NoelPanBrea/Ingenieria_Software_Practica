import sys
import pandas as pd
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHBoxLayout,
    QListWidget, QComboBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class FileLoaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = None

    def initUI(self):
        """
        Configura la interfaz gráfica de usuario (GUI) de la aplicación.
        """
        # Configuración de la ventana principal
        self.setWindowTitle('Lectura de Datasets - GUI')
        self.setGeometry(100, 100, 1200, 800)  # Ventana más grande

        # Estilos de la interfaz gráfica
        self.setStyleSheet("""
            QWidget {
                background-color: #FFCC80;
                font-family: 'Helvetica Neue', sans-serif;
            }
            QPushButton {
                background-color: #FF7043;
                color: #FFF3E0;
                font-size: 18px;
                font-weight: 500;
                padding: 12px 20px;
                border-radius: 12px;
                border: 2px solid #D84315;
            }
            QPushButton:hover {
                background-color: #D84315;
            }
            QLabel {
                font-size: 17px;
                font-weight: 600;
                color: #4E342E;
            }
            QTableWidget {
                background-color: #FFF3E0;
                border: 2px solid #FF7043;
                border-radius: 8px;
                font-size: 14px;
                color: #4E342E;
                font-weight: 700;
            }
            QHeaderView::section {
                background-color: #FFAB91;
                color: #4E342E;
                font-weight: 700;
                border: 1px solid #FF7043;
                padding: 4px;
            }
            QListWidget {
                background-color: #FFF3E0;
                border: 2px solid #FF7043;
                border-radius: 8px;
                font-size: 16px;
                padding: 8px;
                color: #4E342E;
                font-weight: 600;
            }
            QListWidget::item {
                padding: 10px;
                border: 1px solid #FF7043;
                border-radius: 4px;
                margin: 5px 0;
                color: #4E342E;  /* Color del texto */
             
            }
            QComboBox {
                background-color: #FFF3E0;
                border: 2px solid #FF7043;
                border-radius: 8px;
                font-size: 16px;
                padding: 8px;
                color: #4E342E;
                font-weight: 600;
            }
            QListWidget::indicator {
                width: 40px;  
                height: 40px; 
            }
        """)

        # Layout principal
        mainLayout = QVBoxLayout()

        # Layout para botón "Abrir Archivo" y la ruta del archivo
        fileLayout = QHBoxLayout()
        self.loadButton = QPushButton('📂 Abrir Archivo')
        self.loadButton.setFixedWidth(200)
        self.loadButton.setFixedHeight(50)
        self.loadButton.clicked.connect(self.openFileDialog)
        fileLayout.addWidget(self.loadButton)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.filePathLabel = QLabel('Ruta del archivo cargado:')
        fileLayout.addWidget(self.filePathLabel)
        mainLayout.addLayout(fileLayout)

        # Tabla para mostrar los datos
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setMinimumHeight(500) 
        mainLayout.addWidget(self.tableWidget)

        # Selectores de columnas (inicialmente ocultos)
        self.inputLabel = QLabel('Seleccione columnas de entrada (features):')
        self.inputColumnSelector = QListWidget()
        self.inputColumnSelector.setMinimumHeight(150)  # Altura mínima reducida para usar menos espacio
        self.inputColumnSelector.setMaximumHeight(250)  # Altura máxima reducida
        self.outputLabel = QLabel('Seleccione columna de salida (target):')
        self.outputColumnSelector = QComboBox()
        self.confirmButton = QPushButton("Confirmar selección")

        # Ocultar estos elementos inicialmente
        self.inputLabel.hide()
        self.inputColumnSelector.hide()
        self.outputLabel.hide()
        self.outputColumnSelector.hide()
        self.confirmButton.hide()

        # Conectar el cambio de estado del checkbox al método correspondiente
        self.inputColumnSelector.itemChanged.connect(self.onCheckboxChanged)

        # Agregar al layout pero ocultos
        mainLayout.addWidget(self.inputLabel)
        mainLayout.addWidget(self.inputColumnSelector)
        mainLayout.addWidget(self.outputLabel)
        mainLayout.addWidget(self.outputColumnSelector)
        mainLayout.addWidget(self.confirmButton)

        # Conectar el botón de confirmación con la función confirmSelection
        self.confirmButton.clicked.connect(self.confirmSelection)

        # Asignar layout principal
        self.setLayout(mainLayout)

    def openFileDialog(self):
        """
        Muestra el cuadro de diálogo para abrir archivos y carga el archivo seleccionado.
        """
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos CSV (*.csv);;Archivos Excel (*.xlsx *.xls);;Base de datos SQLite (*.sqlite *.db)",
            options=options
        )

        if filePath:
            self.filePathLabel.setText(f'📄 Ruta del archivo cargado: {filePath}')
            self.loadData(filePath)

    def loadData(self, filePath):
        """
        Carga los datos del archivo seleccionado y los muestra en la tabla.
        """
        try:
            if filePath.endswith('.csv'):
                data = pd.read_csv(filePath)
            elif filePath.endswith(('.xlsx', '.xls')):
                data = pd.read_excel(filePath)
            elif filePath.endswith(('.sqlite', '.db')):
                conn = sqlite3.connect(filePath)
                table_data = pd.read_sql_query(
                    "SELECT * FROM sqlite_master WHERE type='table';", conn)
                table_name = table_data.iloc[0]['name']
                data = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
                conn.close()
            else:
                raise ValueError('Formato de archivo no compatible.')

            # Mostrar los datos en la tabla
            self.tableWidget.setRowCount(data.shape[0])
            self.tableWidget.setColumnCount(data.shape[1])
            self.tableWidget.setHorizontalHeaderLabels(data.columns)

            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))
            self.tableWidget.resizeColumnsToContents()

            # Habilitar los selectores de columnas y mostrarlos
            self.enableSelectors(data.columns)

            # Mensaje de éxito
            self.showMessage("✅ ¡Archivo cargado exitosamente! 😃")
            self.data = data
        except Exception as e:
            self.showError(f'⚠ Error al cargar el archivo: {str(e)} ⚠')

    def enableSelectors(self, columns):
        """
        Habilita los selectores de columnas con checkboxes para las columnas de entrada y un combobox para la columna de salida.
        """
        self.inputColumnSelector.clear()
        self.outputColumnSelector.clear()

        # Mostrar selectores y botones
        self.inputLabel.show()
        self.inputColumnSelector.show()
        self.outputLabel.show()
        self.outputColumnSelector.show()
        self.confirmButton.show()

        # Agregar checkboxes a las columnas de entrada
        for index, column in enumerate(columns):
            item = QListWidgetItem(column)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)  # Checkbox no marcado por defecto
            self.inputColumnSelector.addItem(item)

        # Agregar opciones al selector de columna de salida
        self.outputColumnSelector.addItems(columns)

        # Habilitar botones
        self.confirmButton.setEnabled(True)

    def onCheckboxChanged(self, item):
        """
        Cambia el color de la columna correspondiente en la tabla cuando se selecciona o deselecciona un checkbox.
        """
        column_index = self.inputColumnSelector.row(item)  # Obtener el índice de la columna
        if item.checkState() == Qt.Checked:
            # Cambiar color de la columna a naranja
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.item(row, column_index).setBackground(QColor(255,171,145))  # Color naranja
        else:
            # Restaurar color de la columna a blanco
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.item(row, column_index).setBackground(QColor(255,243,224))

    def confirmSelection(self):
        """
        Confirma la selección de columnas y muestra un mensaje con la selección.
        """
        selected_input_columns = [self.inputColumnSelector.item(i).text()
                                  for i in range(self.inputColumnSelector.count())
                                  if self.inputColumnSelector.item(i).checkState() == Qt.Checked]
        output_column = self.outputColumnSelector.currentText()

        if not selected_input_columns:
            self.showError('⚠ Debe seleccionar al menos una columna de entrada. ⚠')
        elif output_column == "":
            self.showError('⚠ Debe seleccionar una columna de salida. ⚠')
        else:
            self.showMessage(f"Columnas de entrada: {', '.join(selected_input_columns)}\nColumna de salida: {output_column} ")

    def showMessage(self, message):
        """
        Muestra un mensaje de éxito en una ventana emergente.
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle("Éxito")
        msgBox.exec_()

    def showError(self, message):
        """
        Muestra un mensaje de error en una ventana emergente.
        """
        errorMsg = QMessageBox()
        errorMsg.setIcon(QMessageBox.Critical)
        errorMsg.setText(message)
        errorMsg.setWindowTitle("Error")
        errorMsg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileLoaderApp()
    ex.show()
    sys.exit(app.exec_())
