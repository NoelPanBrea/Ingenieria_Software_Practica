import dearpygui.dearpygui as dpg

# Ventana principal
def main():
    with dpg.window(label="Ventana Principal", width=400, height=200):
        dpg.add_text("Importar archivo CSV")
        dpg.add_button(label="Importar archivo CSV", callback=open_import_window)
        dpg.add_button(label="Salir", callback=close_main_window)