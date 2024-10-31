import os

class ModelDescription:
    """
    Clase para manejar la persistencia de la descripción del modelo.
    """
    def __init__(self):
        self.description = ""
        # Obtiene el directorio donde está el archivo de código actual
        self.file_path = os.path.join(os.path.dirname(__file__), "descripcion_modelo.txt")

    def save_description(self, description):
        """
        Guarda la descripción en un archivo de texto en el mismo directorio que contiene el script.
        """
        self.description = description
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(self.description)

    def load_description(self):
        """
        Carga la descripción desde el archivo de texto en el mismo directorio, si el archivo existe.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.description = file.read()
        else:
            self.description = ""
        
        return self.description
