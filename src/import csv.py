# Primero hay que ejecutar el comando "pip install pandas" en la terminal

import pandas as pd
import os

# Función para leer un archivo CSV y devolver los datos como un data frame
def load_file(file_path):
    try:

        # Obtener la extensión del archivo y comprobar que sea .csv
        _, extension = os.path.splitext(file_path)
        if extension.lower() != ".csv":  # La convertimos a minúsculas, para evitar confusiones con ".CSV" o ".csv"
            raise ValueError("El archivo no es un CSV.")

        # Leer el archivo CSV usando pandas
        df = pd.read_csv(file_path)
        
        # Comprobar que el data frame no esté vacío
        if df.empty:
            raise ValueError("El archivo CSV no contiene datos.")
        
        #Devolvemos el dataframe
        return df

    # Excepciones en caso de que haya algún error al leer el archivo o que no lo encuentre
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None
    except ValueError as ve:
        print(f"Error: {ve}")
        return None
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None


# Función para obtener las columnas (encabezados) de un archivo CSV
def obtener_columnas_csv(file_path):
    try:
        # Abrir el archivo CSV y leer solo la primera fila
        with open(file_path, 'r') as file:
            # Leer la primera línea del archivo (encabezados)
            primera_fila = file.readline().strip()  # Usamos strip() para eliminar saltos de línea
            
            # Separar los valores por comas y crear una lista con los encabezados
            columnas = primera_fila.split(',')
            return columnas
            
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Error al leer las columnas del archivo CSV: {e}")
        return None
    


if __name__=='__main__':
    print(load_file("C:\\Users\\Usuario\\Downloads\\housing.csv"))
    print("Columnas: ", obtener_columnas_csv("C:\\Users\\Usuario\\Downloads\\housing.csv"))