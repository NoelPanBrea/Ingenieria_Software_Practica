import sys
import pandas as pd
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHBoxLayout, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer


class FileLoaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = None

    def initUI(self):
        '''
            Genera la ventana principal
        '''

        # Configuración de la ventana principal
        self.setWindowTitle('Lectura de Datasets - GUI')
        self.setGeometry(100, 100, 1000, 700)

        # Estilos de la interfaz grafica
        self.setStyleSheet("""   /* Esta parte esta escrita usando CSS */
            QWidget {
                background-color: #FFCC80;  /* Fondo */
                font-family: 'Helvetica Neue', sans-serif;
            }
            QPushButton {
                background-color: #FF7043;  /* Botón */
                color: #FFF3E0;
                font-size: 18px;
                font-weight: 500;
                padding: 12px 20px;
                border-radius: 12px;
                border: 2px solid #D84315;  /* Borde del botón */
            }
            QPushButton:hover {
                background-color: #D84315;  /* Botón pulsado */
            }
            QLabel {
                font-size: 17px;
                font-weight: 600;
                color: #4E342E;  /* Texto (titulo y path) */
            }
            QTableWidget {
                background-color: #FFF3E0;  /* Fondo tabla */
                border: 2px solid #FF7043;  /* Borde tabla */
                border-radius: 8px;
                font-size: 14px;
                color: #4E342E;  /* Texto tabla */
            }
            QHeaderView::section {
                background-color: #FFAB91;  /* Fondo encabezados */
                color: #4E342E;  /* Texto encabezados */
                font-weight: 700; 
                border: 1px solid #FF7043;  /* Borde encabezados */
                padding: 4px;
            }
            QProgressBar {
                border: 2px solid #D84315;  /* Borde barra de carga */
                border-radius: 5px;
                text-align: center;
                color: white;
                background-color: #FFCC80;  /* Fondo barra de carga */
            }
        """)

        # Layout vertical
        mainLayout = QVBoxLayout()

        # Título de la aplicación
        titleLabel = QLabel(" Explorador de archivos ")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("padding: 7px;")
        mainLayout.addWidget(titleLabel)  # Añadimos el titulo

        # Botón para añadir archivos
        self.loadButton = QPushButton('📂 Abrir Archivo')
        self.loadButton.setFixedWidth(200)
        self.loadButton.setFixedHeight(50)
        # AL clicar el boton llamamos a la funcion que carga los archivos
        self.loadButton.clicked.connect(self.openFileDialog)
        # Usamos un layout horizontal para centrar el boton añadiendo espacio a los lados
        loadButtonLayout = QHBoxLayout()
        loadButtonLayout.addStretch(1)
        loadButtonLayout.addWidget(self.loadButton)
        loadButtonLayout.addStretch(1)
        mainLayout.addLayout(loadButtonLayout)

        # Etiqueta para mostrar la ruta del archivo cargado
        self.filePathLabel = QLabel('Ruta del archivo cargado:')
        self.filePathLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.filePathLabel)

        # Barra de carga
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        mainLayout.addWidget(self.progressBar)

        # Tabla para mostrar los datos
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # No permite editar los datos
        mainLayout.addWidget(self.tableWidget)

        # Mensaje carga exitosa
        self.successLabel = QLabel('')
        self.successLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.successLabel)

        # Asignamos el layout principal
        self.setLayout(mainLayout)

    def openFileDialog(self):
        """
        Optiene el path del archivo e inicia la barra de progreso
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
            self.filePathLabel.setText(
                f'📄 Ruta del archivo cargado: {filePath}')
            self.successLabel.setText("Cargando archivo ... 💿")
            self.successLabel.setStyleSheet("color: #4E342E; font-size: 16px;")
            self.startProgressBar()  # Iniciamos el progreso de la barra
            QTimer.singleShot(2000, lambda: self.loadData(
                filePath))  # Simular el tiempo de carga

    def startProgressBar(self):
        """
        Simula el progreso de la barra de carga
        """
        self.progressBar.setValue(0)
        for i in range(1, 101):
            QTimer.singleShot(i * 20, lambda v=i: self.progressBar.setValue(v))

    def loadData(self, filePath):
        """
            Carga los datos del archivo y los muestra en una tabla
        """
        try:
            # Detectar el tipo de archivo y cargarlo
            if filePath.endswith('.csv'):
                data = pd.read_csv(filePath)
            elif filePath.endswith(('.xlsx', '.xls')):
                data = pd.read_excel(filePath)
            elif filePath.endswith(('.sqlite', '.db')):
                conn = sqlite3.connect(filePath)
                data = pd.read_sql_query(
                    "SELECT * FROM sqlite_master WHERE type='table';", conn)
                table_name = data.iloc[0]['name']
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
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(data.iat[i, j])))
            self.tableWidget.resizeColumnsToContents()
            self.successLabel.setText("✅ ¡Archivo cargado exitosamente! 😃")
            self.successLabel.setStyleSheet("color: green; font-size: 16px;")
            self.data = data
        except Exception as e:
            self.showError(f'⚠ Error al cargar el archivo: {str(e)} ⚠')

    def showError(self, message):
        """
        Ventana en caso de error
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
