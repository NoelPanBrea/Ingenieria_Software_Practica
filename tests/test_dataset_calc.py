import pytest
import pandas as pd
from pandas import DataFrame
from src.data_processing.dataset_calc import PreprocessApplier, none_count 

# Datos de prueba
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "col1": [1, None, 3, None],
        "col2": [None, 2, 3, 4],
        "col3": [1, None, None, 4]
    })

# Pruebas para el método delete
def test_delete(sample_dataframe):
    preprocessor = PreprocessApplier()
    preprocessor.set_current_method("delete")
    preprocessor.apply_preprocess(sample_dataframe, ["col1", "col2"])
    assert sample_dataframe.shape[0] == 1  # Quedan solo las filas sin valores nulos

# Pruebas para el método mean
def test_mean(sample_dataframe):
    preprocessor = PreprocessApplier()
    preprocessor.set_current_method("mean")
    preprocessor.apply_preprocess(sample_dataframe, ["col1", "col2"])
    assert sample_dataframe["col1"].isna().sum() == 0
    assert sample_dataframe["col2"].isna().sum() == 0
    assert sample_dataframe["col1"].iloc[1] == pytest.approx(2)  # Media calculada

# Pruebas para el método median
def test_median(sample_dataframe):
    preprocessor = PreprocessApplier()
    preprocessor.set_current_method("median")
    preprocessor.apply_preprocess(sample_dataframe, ["col1", "col2"])
    assert sample_dataframe["col1"].isna().sum() == 0
    assert sample_dataframe["col2"].isna().sum() == 0
    assert sample_dataframe["col1"].iloc[1] == 3.0  # Mediana calculada

# Pruebas para el método constant
def test_constant(sample_dataframe):
    preprocessor = PreprocessApplier()
    preprocessor.set_current_method("constant", cte=[0, -1])
    preprocessor.apply_preprocess(sample_dataframe, ["col1", "col2"])
    assert (sample_dataframe["col1"] == 0).sum() == 2
    assert (sample_dataframe["col2"] == -1).sum() == 1

# Pruebas de manejo de errores
def test_invalid_method(sample_dataframe):
    preprocessor = PreprocessApplier()
    with pytest.raises(KeyError):
        preprocessor.set_current_method("invalid")

def test_missing_cte(sample_dataframe):
    preprocessor = PreprocessApplier()
    preprocessor.set_current_method("constant", cte=[0]) 
    with pytest.raises(ValueError):
        preprocessor.apply_preprocess(sample_dataframe, ["col1", "col2"])

def test_none_count(sample_dataframe):
    result = none_count(sample_dataframe, ["col1", "col2", "col3"])
    assert result == [2, 1, 2]
