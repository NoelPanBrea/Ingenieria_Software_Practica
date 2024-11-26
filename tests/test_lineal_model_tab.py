import pytest
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QApplication)
from unittest.mock import MagicMock
from src.models.lineal_model import LinealModel
from src.tabs.lineal_model_tab import LinealModelTab
from src.ui.popup_handler import show_error, show_message
import numpy as np
import joblib


@pytest.fixture
def app(qtbot):
    """Fixture to initialize the QApplication"""
    app = QApplication([])
    return app


@pytest.fixture
def model_data():
    """Fixture to provide mock model data"""
    return {
        'formula': 'y = 2.5 * x + 5',
        'metrics': {'r2_score': 0.95, 'rmse': 0.2},
        'description': 'This is a linear regression model.',
        'columns': {'input': ['x'], 'output': 'y'}
    }


@pytest.fixture
def lineal_model_tab(mocker, model_data):
    """Fixture to create an instance of LinealModelTab"""
    mocker.patch('models.lineal_model.LinealModel', autospec=True)  # Mock the LinealModel class
    mocker.patch('ui.popup_handler.show_error', autospec=True)
    mocker.patch('ui.popup_handler.show_message', autospec=True)

    tab = LinealModelTab(data=None, input_columns=['x'], output_column='y')
    tab.setup_model_display(model_data)  # Setting up a mock model
    return tab


def test_model_creation(lineal_model_tab, mocker):
    """Test if model creation works"""
    # Mock the model fitting behavior
    mock_model = MagicMock(spec=LinealModel)
    lineal_model_tab.model = mock_model
    mock_model.fit.return_value = None  # Simulate model fitting

    # Trigger model creation
    lineal_model_tab.create_model()

    # Verify that the fit method was called
    mock_model.fit.assert_called_once()


def test_show_model_data(lineal_model_tab, model_data):
    """Test if model data is displayed correctly"""
    lineal_model_tab.setup_model_display(model_data)

    # Verify the text of formula, R2, and MSE labels
    assert lineal_model_tab.formula_label.text() == f"Fórmula del Modelo: {model_data['formula']}"
    assert lineal_model_tab.r2_label.text() == f"R²: {model_data['metrics']['r2_score']:.4f}"
    assert lineal_model_tab.mse_label.text() == f"ECM: {model_data['metrics']['rmse']:.4f}"


def test_save_model(lineal_model_tab, model_data, mocker):
    """Test saving model data"""
    mocker.patch('joblib.dump')  # Mocking joblib.dump to avoid actual file saving
    mocker.patch('ui.popup_handler.save_file_dialog', return_value="mock_path.pkl")  # Mock file dialog

    # Simulate a loaded model for saving
    lineal_model_tab.model = MagicMock(spec=LinealModel)
    lineal_model_tab.model.coef_ = np.array([2.5])
    lineal_model_tab.model.intercept_ = 5
    lineal_model_tab.model.formula = model_data['formula']
    lineal_model_tab.model_description.set_description(model_data['description'])

    lineal_model_tab.save_model()

    # Verify that joblib.dump was called with the correct model data
    joblib.dump.assert_called_once_with(
        {
            'formula': model_data['formula'],
            'coefficients': lineal_model_tab.model.coef_.tolist(),
            'intercept': lineal_model_tab.model.intercept_,
            'description': model_data['description'],
            'metrics': model_data['metrics'],
            'columns': model_data['columns']
        },
        "mock_path.pkl"
    )
    show_message.assert_called_once_with("✅ ¡Modelo guardado exitosamente! 😃")


def test_make_prediction(lineal_model_tab, mocker):
    """Test making predictions with the model"""
    # Mock model's prediction behavior
    mocker.patch.object(lineal_model_tab.model, 'predict', return_value=10.0)

    # Prepare mock input values for prediction
    lineal_model_tab.input_widgets = [
        (QLabel("x:"), QLineEdit("3"))
    ]
    
    lineal_model_tab.make_prediction()

    # Verify prediction result is displayed correctly
    assert lineal_model_tab.prediction_label.text() == "Resultado de la Predicción:\n y = 10.0000"
    assert lineal_model_tab.prediction_label.isVisible()


def test_invalid_prediction_input(lineal_model_tab, mocker):
    """Test invalid input during prediction"""
    mocker.patch.object(lineal_model_tab.model, 'predict', return_value=10.0)

    # Prepare an invalid input (non-numeric value)
    lineal_model_tab.input_widgets = [
        (QLabel("x:"), QLineEdit("invalid"))
    ]
    
    lineal_model_tab.make_prediction()

    # Check that an error is shown due to invalid input
    show_error.assert_called_once_with("El valor para x: debe ser numérico.", lineal_model_tab)
    

def test_model_loading(lineal_model_tab, mocker, model_data):
    """Test loading a pre-trained model"""
    loaded_model = {
        'formula': model_data['formula'],
        'metrics': model_data['metrics'],
        'description': model_data['description'],
        'columns': model_data['columns'],
        'coefficients': [2.5],
        'intercept': 5.0
    }

    lineal_model_tab.initialize_from_loaded_model(loaded_model)

    # Verify that the model data is correctly loaded and displayed
    assert lineal_model_tab.formula_label.text() == f"Fórmula del Modelo: {model_data['formula']}"
    assert lineal_model_tab.r2_label.text() == f"R²: {model_data['metrics']['r2_score']:.4f}"
    assert lineal_model_tab.mse_label.text() == f"ECM: {model_data['metrics']['rmse']:.4f}"


@pytest.mark.parametrize("input_values, expected_output", [
    ([2], 12.0),  
    ([3], 15.5),
])
def test_prediction_with_various_inputs(lineal_model_tab, input_values, expected_output, mocker):
    """Test making predictions with various inputs"""
    mocker.patch.object(lineal_model_tab.model, 'predict', return_value=10.0)

    # Simulate valid inputs for prediction
    for i, value in enumerate(input_values):
        lineal_model_tab.input_widgets[i][1].setText(str(value))

    lineal_model_tab.make_prediction()

    # Check that the predicted value matches expected output
    assert lineal_model_tab.prediction_label.text() == f"Resultado de la Predicción:\n y = {expected_output:.4f}"


