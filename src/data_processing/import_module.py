from pandas import DataFrame, read_csv, read_excel, read_sql
import sqlite3


def load_file(file_path: str) -> DataFrame:
    """
    Loads a .sql, .db, .csv, .xls, or .xlsx file.

    Parameters 
    -----------
    file_path : str
        Path to the desired file.

    Returns
    -----------
     data: DataFrame
        Data in a DataFrame.
    """

    # Obtain the file's extension
    try:
        if file_path.lower().endswith(".csv"):
            data = __import_csv(file_path)
        elif file_path.lower().endswith((".xlsx", ".xls")):
            data = __import_excel(file_path)
        elif file_path.lower().endswith((".sqlite", ".db")):
            data = __import_sql(file_path)
        else:
            raise ValueError("Formato de archivo no soportado")

        return data
    # Error managing: File reading error
    except ValueError as e:
        raise ValueError(f"Error al cargar el archivo: {e}")
    # Error managing: File not found error
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Archivo no encontrado: {e}")
    # Error managing: Unexpected exceptions
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")


def __import_sql(file_path: str) -> DataFrame:
    """
    Loads data from the first table of a SQL file.

    Parameters 
    -----------
    file_path: str
        Path to the .sql/.db file.

    Returns
    -----------
     data: DataFrame
        Data in a DataFrame.

    Raises
    -----------
    ValueError: If the database is empty or cannot be loaded
    """
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # Obtain the name of the first table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchone()

        # Check if any tables exist
        if result is None:
            conn.close()
            raise ValueError("La base de datos no contiene ninguna tabla")

        table_name = result[0]

        # Load the data from the table to the DataFrame
        query = f"SELECT * FROM {table_name}"
        data = read_sql(query, conn)

        conn.close()
        return data
    except Exception as e:
        raise ValueError(f"Error al cargar la base de datos SQLite: {e}")


def __import_excel(file_path: str) -> DataFrame:
    """
    Loads data from an Excel file.

    Parameters 
    -----------
    file_path: str
        Path to the .xls/.xlsx file.

    Returns
    -----------
     data: DataFrame
        Data in a DataFrame.
    """
    try:
        # Read excel file
        data = read_excel(file_path)
        if data.empty:
            raise ValueError(f"Documento excel vacio")
        return data

    except Exception as e:
        raise ValueError(f"Error al cargar el archivo excel: {e}")
    # Needed in order to work: pip install pandas openpyxl xlrd


def __import_csv(file_path: str) -> DataFrame:
    """
    Loads data from a CSV file.

    Parameters 
    -----------
    file_path: str
        Path to the .csv file.

    Returns
    -----------
     data: DataFrame
        Data in a DataFrame.
    """
    try:
        # Read csv file
        data = read_csv(file_path)
        return data

    except ValueError as e:
        raise ValueError(
            f"Error al cargar el archivo CSV: Documento CSV vacio")
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo CSV: {e}")
