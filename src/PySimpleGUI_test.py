# Es necesario instalar el módulo mediante el comando "pip install pysimplegui"

import PySimpleGUI as sg

# Tema
sg.theme('DarkTeal9')


# Ventana 2
def import_window():
    layout1 = [
        [sg.Text('Introduzca aquí debajo la ruta del archivo csv que desea importar')],
        [sg.InputText()],
        [sg.Button('Ok')]
    ]
    window1 =sg.Window('TEST2', layout1)
    while True:
        event, values = window1.read()
        if event == sg.WINDOW_CLOSED or event == 'OK': 
            break
            
    window1.close()


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