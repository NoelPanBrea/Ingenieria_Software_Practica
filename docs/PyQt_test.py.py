import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

def crear_interfaz():
    # Función para mostrar el mensaje de texto
    def mostrar_mensaje():
        texto = entrada.text()  # Obtener el texto ingresado en el cuadro de texto
        if texto:
            QMessageBox.information(None, "Mensaje", f"Texto ingresado: {texto}")
        else:
            QMessageBox.warning(None, "Advertencia", "Por favor, ingrese algún texto.")

    # Crear la aplicación
    app = QApplication(sys.argv)

    # Crear la ventana principal
    ventana = QWidget()
    ventana.setWindowTitle("Interfaz Gráfica PyQt")
    ventana.setGeometry(100, 100, 400, 200)  # Tamaño de la ventana
    ventana.setStyleSheet("background-color: #e6f7ff;")  # Fondo de la ventana

    # Crear un layout vertical para organizar los elementos
    layout = QVBoxLayout()

    # Título ventana
    titulo = QLabel("Bienvenido")
    titulo.setFont(QFont("Arial", 18, QFont.Bold))
    titulo.setAlignment(Qt.AlignCenter)
    titulo.setStyleSheet("color: #333;")
    layout.addWidget(titulo) # ponemos el titulo en el layout vertical

    # Cuadro de texto
    entrada = QLineEdit()
    entrada.setPlaceholderText("Ingresa tu texto aquí...")
    entrada.setFont(QFont("Arial", 12))
    entrada.setStyleSheet("padding: 5px;")
    layout.addWidget(entrada)

    # Botón
    boton = QPushButton("Mostrar Mensaje")
    boton.setFont(QFont("Arial", 12, QFont.Bold))
    boton.setStyleSheet("""
        background-color: #0099cc;
        color: white;
        padding: 8px;
        border-radius: 5px; 
    """) #se pueden redondear las esquinas
    boton.clicked.connect(mostrar_mensaje)
    layout.addWidget(boton)

    # Crear una etiqueta de pie de página
    pie_de_pagina = QLabel("Ingresa tu texto y presiona el botón")
    pie_de_pagina.setFont(QFont("Arial", 10))
    pie_de_pagina.setAlignment(Qt.AlignCenter)
    pie_de_pagina.setStyleSheet("color: #666;")
    layout.addWidget(pie_de_pagina)

    # Establecer el layout en la ventana
    ventana.setLayout(layout)

    # Mostrar la ventana
    ventana.show()

    # Ejecutar el loop principal de la aplicación
    sys.exit(app.exec_())

if __name__=='__main__':
    crear_interfaz()