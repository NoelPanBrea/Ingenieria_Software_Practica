import pytest
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from src.models.linear_model import LinearModel
from pathlib import Path

# Añadir el directorio src al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

@pytest.fixture
def sample_data():
    """Create a sample dataset for testing."""
    data = pd.DataFrame({
        'x1': [1, 2, 3, 4, 5],
        'x2': [2, 4, 5, 4, 5],
        'y': [3, 7, 11, 13, 17]
    })
    return data

@pytest.fixture
def linear_model(sample_data):
    """Create a LinearModel instance with sample data."""
    return LinearModel(
        data=sample_data, 
        input_columns=['x1', 'x2'], 
        output_column='y'
    )

def test_initialization(sample_data):
    """Test the initialization of LinearModel."""
    model = LinearModel(
        data=sample_data, 
        input_columns=['x1', 'x2'], 
        output_column='y'
    )
    
    # Check initial attributes
    assert model.data is not None
    assert model.input_columns == ['x1', 'x2']
    assert model.output_column == 'y'
    assert model.x is not None
    assert model.y is not None
    
    # Check model placeholders
    assert model.coef_ is None
    assert model.intercept_ is None
    assert model.y_pred is None
    assert model.mse_ is None
    assert model.r2_ is None
    assert model.formula is None

def test_set_model_params(linear_model):
    """Test setting model parameters manually."""
    coefficients = [2.0, 3.0]
    intercept = 1.0
    formula = "y = 1.00 + (2.00 * x1) + (3.00 * x2)"
    
    linear_model.set_model_params(coefficients, intercept, formula)
    
    assert np.array_equal(linear_model.coef_, coefficients)
    assert linear_model.intercept_ == intercept
    assert linear_model.formula == formula

def test_fit_method(linear_model):
    """Test the fit method of the LinearModel."""
    # Fit the model
    linear_model.fit()
    
    # Assertions
    assert linear_model.coef_ is not None
    assert linear_model.intercept_ is not None
    assert linear_model.y_pred is not None
    assert linear_model.mse_ is not None
    assert linear_model.r2_ is not None
    assert linear_model.formula is not None

def test_evaluate_method(linear_model):
    """Test the model evaluation method."""
    # Fit the model first
    linear_model.fit()
    
    # Assertions about evaluation metrics
    assert 0 <= linear_model.r2_ <= 1
    assert linear_model.mse_ >= 0

def test_evaluate_method_without_fit(linear_model):
    """Test evaluation method raises error when predictions are not generated."""
    # Reset predictions to None to simulate not calling fit
    linear_model.y_pred = None
    
    # Should raise a ValueError
    with pytest.raises(ValueError, match="Predicciones no generadas"):
        linear_model.evaluate()

def test_calc_formula(linear_model):
    """Test the formula calculation method."""
    # Fit the model first
    linear_model.fit()
    
    # Verify formula structure
    assert linear_model.formula.startswith('y = ')
    assert 'x1' in linear_model.formula
    assert 'x2' in linear_model.formula
    
    # Check number of terms
    terms = linear_model.formula.split(' + ')
    assert len(terms) == 3  # Intercept + two input columns

def test_zero_input_data():
    """Test model behavior with zero input data."""
    data = pd.DataFrame({
        'x1': [0, 0, 0],
        'x2': [0, 0, 0],
        'y': [0, 0, 0]
    })
    
    model = LinearModel(
        data=data, 
        input_columns=['x1', 'x2'], 
        output_column='y'
    )
    
    # Should not raise any errors
    model.fit()
    
    assert model.coef_ is not None
    assert model.intercept_ is not None