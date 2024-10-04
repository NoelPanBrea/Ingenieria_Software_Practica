import os
import sys
import pandas as pd

def import_file():
    # Verificar si se ha insertado el nombre del archivo
    if len(sys.argv) != 2:
        raise ValueError("No se ha insertado el nombre del archivo")
    
    # Obtener el archivo
    file = sys.argv[1]

    # Obtener la extensión del archivo
    _, extension = os.path.splitext(file)

    # Identificar si es un archivo de Excel y leer las primeras filas
    if extension in ['.xls', '.xlsx']:
        try:
            # Leer el archivo de Excel
            excel = pd.read_excel(file)
            # Verificar si hay tabla
            if excel.empty:
                raise ValueError("En el archivo Excel no hay tabla")
            # Mostrar las primeras 5 filas
            print(excel.head())
            
        #Manejar los errores: lectura del archivo
        except ValueError as e:
            raise ValueError(f"Error al leer el archivo de Excel: {e}")
        #Manejar los errores: ruta del archivo
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Archivo no encontrado: {e}")
        #Manejar los errores inesperados
        except Exception as e:
            print(f"Se produjo un error inesperado: {e}")
            
    #Devolver el archivo para futuras operaciones
    return file

#NECESARIO PARA QUE FUNCIONE: pip install pandas openpyxl xlrd

if __name__ == "__main__":
    import_file()