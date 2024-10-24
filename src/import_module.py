import pandas as pd
import sqlite3
import os
from tkinter import filedialog


def load_file(file_path: str) -> pd.DataFrame:
    """
    Loads a .sql, .db, .csv, .xls, .xlsx file

    Parameters 
    -----------
    file_path : str
        Desired file's path

    Returns
    -----------
     data: Dataframe
        Data in a pd.DataFrame
    """

    # Obtain the file's extension
    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension in [".sqlite", ".db"]:
            data = import_sql(file_path)
        elif extension in [".xlx", ".xlsx"]:
            data = import_excel(file_path)
        elif extension in [".csv"]:
            data = import_csv(file_path)
        else:
            raise ValueError('Formato de archivo no soportado')

        # Verify there was data in the file
        if data.empty:
            raise ValueError("En el archivo no hay tabla")
        print("\nDatos cargados correctamente. Primeras filas:\n")
        return data
    # Error managing: lectura del archivo
    except ValueError as e:
        raise ValueError(f"Error al leer el archivo de Excel: {e}")
    # Error managing:
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Archivo no encontrado: {e}")
    # Error managing: Unexpected exceptions
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")


def import_sql(file_path: str) -> pd.DataFrame:
    """
    Loads data from the first table of a sql file

    Parameters 
    -----------
    file_path: str
        File_path to the .sql/.db file

    Returns
    -----------
     data: Dataframe
        Data in a  pd.DataFrame
    """
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # Obtain the name of the first table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = cursor.fetchone()[0]

        # Load the data from the table to the DataFrame
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)

        conn.close()
        return data
    except Exception as e:
        raise ValueError(f"Error al cargar la base de datos SQLite: {e}")


def import_excel(file_path: str) -> pd.DataFrame:
    """
    Loads data from a excel file

    Parameters 
    -----------
    file_path: str
        File_path to the .xlx/.xlxs file

    Returns
    -----------
     data: Dataframe
        Data in a pd.DataFrame
    """
    try:
        # Read excel file
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo excel: {e}")
    # Needed in order to work: pip install pandas openpyxl xlrd


def import_csv(file_path: str) -> pd.DataFrame:
    """
    Loads data from a csv file

    Parameters 
    -----------
    file_path: str
        File_path to the .csv file

    Returns
    -----------
     data: Dataframe
        Data in a pd.DataFrame
    """
    try:
        # Read csv file
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo excel: {e}")
