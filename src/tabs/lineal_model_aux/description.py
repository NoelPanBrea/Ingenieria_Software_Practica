import os

class ModelDescription:
    """
    Clase para manejar la persistencia de la descripción del modelo.
    """
    def __init__(self):
        self.description = ""
        # Obtiene el directorio donde está el archivo de código actual
        self.file_path = os.path.join(os.path.dirname(__file__), "descripcion_modelo.txt")
        
    def load_description(self):
        """
        Carga la descripción desde el archivo de texto en el mismo directorio, si el archivo existe.
        Si ocurre un error de lectura, lo maneja sin interrumpir la ejecución.
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.description = file.read()
            else:
                self.description = ""
        except IOError as e:
            print(f"Error al cargar la descripción: {e}")
            self.description = ""  # Restablece la descripción en caso de error
        
        return self.description

    
        self.description_display.show()


