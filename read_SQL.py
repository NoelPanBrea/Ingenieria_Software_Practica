import pandas as pd
import sqlite3
import os
from tkinter import filedialog

def cargar_archivo(file_path):
    """
    Carga una base de datos SQLite y muestra las primeras filas de los datos.
    
    Parameters 
    -----------
    file_path : str
        Direccion del archivo

    Returns
    -----------
     data: Dataframe
        Datos en un dataframe de pandas
    """
    extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if extension in [".sqlite", ".db"]:
            data = cargar_sqlite(file_path)
        else:
            raise ValueError("Formato de archivo no soportado")
        
        print("\nDatos cargados correctamente. Primeras filas:\n")
        print(data.head())  # Muestra las primeras filas de los datos
        return data
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")

def cargar_sqlite(db_path):
    """
    Carga los datos de la primera tabla de una base de datos SQLite.

    Parameters 
    -----------
    db_path : str
        Direccion del archivo SQLite

    Returns
    -----------
     data: Dataframe
        Datos en un dataframe de pandas
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener el nombre de la primera tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = cursor.fetchone()[0]
        
        # Cargar los datos de la tabla en un DataFrame
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)
        
        conn.close()
        print(type(data))
        return data
    
    except Exception as e:
        raise ValueError(f"Error al cargar la base de datos SQLite: {e}")


if __name__=='__main__':
    path = filedialog.askopenfilename(title='elige el archivo que quieres abrir',filetypes=[('Archivo SQL','*.sqlite')])
    datos = cargar_archivo(path)

