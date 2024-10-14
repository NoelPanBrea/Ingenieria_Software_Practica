import dearpygui.dearpygui as dpg


# Callback para la ventana de importar archivo CSV
def open_import_window(sender, app_data, user_data):
    with dpg.window(label="Importar archivo CSV", modal=True, width=400, height=200) as import_window:
        dpg.add_text("Introduzca aquí debajo la ruta del archivo CSV que desea importar:")
        input_text = dpg.add_input_text(label="Ruta del CSV")
        dpg.add_button(label="OK", callback=lambda: close_import_window(import_window))

def close_import_window(window):
    dpg.delete_item(window)


# Callback para cerrar la aplicación
def close_main_window(sender, app_data, user_data):
    dpg.stop_dearpygui()


# Ventana principal
def main():
    with dpg.window(label="Ventana Principal", width=400, height=200):
        dpg.add_text("Importar archivo CSV")
        dpg.add_button(label="Importar archivo CSV", callback=open_import_window)
        dpg.add_button(label="Salir", callback=close_main_window)