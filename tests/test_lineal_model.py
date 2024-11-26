import pytest
import pandas as pd
import numpy as np
from models.lineal_model import LinealModel, create_graphic

# Datos de ejemplo para las pruebas
@pytest.fixture
def sample_data():
    data = {
        "X1": [1, 2, 3, 4, 5],
        "Y": [2.2, 4.1, 6.0, 8.2, 10.1]
    }
    return pd.DataFrame(data)

@pytest.fixture
def lineal_model(sample_data):
    return LinealModel(sample_data, input_columns=["X1"], output_column="Y")

def test_init(lineal_model, sample_data):
    """Prueba la inicialización del modelo."""
    assert lineal_model.data.equals(sample_data)
    assert lineal_model.input_columns == ["X1"]
    assert lineal_model.output_column == "Y"
    assert lineal_model.x.shape == (5, 1)
    assert lineal_model.y.shape == (5,)
    assert lineal_model.coef_ is None
    assert lineal_model.intercept_ is None

def test_fit(lineal_model):
    """Prueba el ajuste del modelo."""
    lineal_model.fit()
    assert lineal_model.coef_ is not None
    assert lineal_model.intercept_ is not None
    assert lineal_model.y_pred is not None
    assert lineal_model.mse_ is not None
    assert lineal_model.r2_ is not None
    assert isinstance(lineal_model.formula, str)

def test_predict(lineal_model):
    """Prueba la predicción del modelo."""
    lineal_model.fit()
    predictions = lineal_model.predict()
    assert predictions.shape == lineal_model.y.shape
    assert np.allclose(predictions, lineal_model.y_pred)

def test_evaluate(lineal_model):
    """Prueba la evaluación del modelo."""
    lineal_model.fit()
    mse = lineal_model.mse_
    r2 = lineal_model.r2_
    assert mse > 0
    assert 0 <= r2 <= 1

def test_calc_formula(lineal_model):
    """Prueba el cálculo de la fórmula de regresión lineal."""
    lineal_model.fit()
    formula = lineal_model.formula
    assert formula.startswith("Y =")
    assert "X1" in formula

def test_set_model_params(lineal_model):
    """Prueba la configuración manual de parámetros del modelo."""
    coefficients = [2.0]
    intercept = 1.0
    formula = "Y = 1.0 + 2.0 * X1"
    lineal_model.set_model_params(coefficients, intercept, formula)
    assert lineal_model.coef_ == coefficients
    assert lineal_model.intercept_ == intercept
    assert lineal_model.formula == formula

#CAMBIAR POR PRUEBA DE GRÁFICA 3D
"""
def test_create_graphic(sample_data):
    ""Prueba la creación de la gráfica sin errores.""
    x = sample_data["X1"].values.reshape(-1, 1)
    y = sample_data["Y"].values
    model = LinealModel(sample_data, ["X1"], "Y")
    model.fit()
    y_pred = model.y_pred

    try:
        create_graphic(x, y, y_pred, ["X1"], "Y")
    except Exception as e:
        pytest.fail(f"create_graphic lanzó una excepción: {e}")
"""