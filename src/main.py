import os
import sys
import pandas as pd

def import_file():
    # Obtener el archivo
    file = sys.argv[1]
    # Obtener la extensión del archivo
    _, extension = os.path.splitext(file)

    # Identificar si es un archivo de Excel y leer las primeras filas
    if extension in ['.xls', '.xlsx']:
        try:
            # Leer el archivo de Excel
            excel = pd.read_excel(file)
            
            # Mostrar las primeras 5 filas
            print(excel.head())
        except Exception as e:
            print(f"Error al leer el archivo de Excel: {e}")
            
    #Devolver el archivo para futuras operaciones
    return file

#NECESARIO PARA QUE FUNCIONE: pip install pandas openpyxl xlrd

if __name__ == "__main__":
    import_file()