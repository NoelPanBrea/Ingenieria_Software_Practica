# Es necesario instalar el módulo mediante el comando "pip install pysimplegui"

import PySimpleGUI as sg

# Tema
sg.theme('DarkTeal9')


# Ventana principal
def main():
    layout = [
        [sg.Text('Importar archivo CSV')],
        [sg.Button('Importar archivo CSV'), sg.Button('Salir')]
    ]
    window =sg.Window('TEST', layout)
    while True:
        event, values = window.read()
        if event == 'Salir' or event == sg.WINDOW_CLOSED:
            break
        if event == 'Importar archivo CSV':
            import_window()
            
    window.close()