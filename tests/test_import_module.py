import pytest
import sqlite3
from pandas import DataFrame
from src.data_processing.import_module import load_file, __import_csv, __import_excel, __import_sql
import os

# Fixtures para datos de prueba
@pytest.fixture
def csv_file(tmpdir):
    file = tmpdir.join("test.csv")
    file.write("col1,col2\nval1,val2")
    return str(file)

@pytest.fixture
def excel_file(tmpdir):
    file = tmpdir.join("test.xlsx")
    data = DataFrame({"col1": ["val1"], "col2": ["val2"]})
    data.to_excel(file, index=False)
    return str(file)

@pytest.fixture
def sqlite_file(tmpdir):
    file = tmpdir.join("test.db")
    import sqlite3
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test_table (col1 TEXT, col2 TEXT)")
    cursor.execute("INSERT INTO test_table (col1, col2) VALUES ('val1', 'val2')")
    conn.commit()
    conn.close()
    return str(file)

# Pruebas para `load_file`
def test_load_csv(csv_file):
    data = load_file(csv_file)
    assert isinstance(data, DataFrame)
    assert data.shape == (1, 2)
    assert list(data.columns) == ["col1", "col2"]

def test_load_excel(excel_file):
    data = load_file(excel_file)
    assert isinstance(data, DataFrame)
    assert data.shape == (1, 2)
    assert list(data.columns) == ["col1", "col2"]

def test_load_sql(sqlite_file):
    data = load_file(sqlite_file)
    assert isinstance(data, DataFrame)
    assert data.shape == (1, 2)
    assert list(data.columns) == ["col1", "col2"]

# Pruebas para errores esperados
def test_load_unsupported_file():
    with pytest.raises(ValueError, match="Formato de archivo no soportado"):
        load_file("unsupported.txt")

def test_load_empty_sqlite(tmpdir):
    empty_db = tmpdir.join("empty.db")
    conn = sqlite3.connect(empty_db)
    conn.close()
    with pytest.raises(ValueError, match="En el archivo no hay tabla"):
        load_file(str(empty_db))

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_file("nonexistent.csv")
