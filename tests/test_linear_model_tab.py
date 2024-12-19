import pytest
from PyQt5.QtWidgets import QApplication
import sys
import numpy as np
from pathlib import Path
import joblib
from unittest.mock import MagicMock, patch
import pandas as pd
from src.tabs.linear_model_tab import LinearModelTab
from src.models.linear_model import LinearModel

# Añadir el directorio src al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

@pytest.fixture(scope="module")
def qapp():
    """Fixture para la aplicación Qt a nivel de módulo"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

@pytest.fixture
def sample_data():
    """Fixture para crear datos de prueba"""
    # Crear datos simples para regresión lineal
    np.random.seed(42)
    X = np.array([[1], [2], [3], [4], [5]])
    y = 2 * X.ravel() + 1 + np.random.normal(0, 0.1, 5)
    return pd.DataFrame(X, columns=['x']), pd.Series(y.ravel(), name='y')

@pytest.fixture
def linear_model_tab(qapp, sample_data):
    """Fixture para el LinearModelTab con datos de prueba"""
    X, y = sample_data
    tab = LinearModelTab(
        data=X.join(y),
        input_columns=['x'],
        output_column='y'
    )
    # Mockear componentes de UI que pueden causar problemas
    tab.plot_manager = MagicMock()
    tab.model_description = MagicMock()
    tab.model_description.get_description.return_value = "Test model description"
    return tab

def test_create_model(linear_model_tab):
    """Test de creación del modelo"""
    # Mockear show_message para evitar diálogos
    with patch('tabs.linear_model_tab.show_message'):
        # Crear el modelo
        linear_model_tab.create_model()
        
        # Verificar que el modelo se creó correctamente
        assert linear_model_tab.model is not None
        assert isinstance(linear_model_tab.model, LinearModel)
        assert hasattr(linear_model_tab.model, 'coef_')
        assert hasattr(linear_model_tab.model, 'intercept_')
        
        # Verificar que los coeficientes son razonables (cerca de 2 y 1 según los datos de prueba)
        assert abs(linear_model_tab.model.coef_[0] - 2) < 0.5
        assert abs(linear_model_tab.model.intercept_ - 1) < 0.5

def test_make_prediction(linear_model_tab):
    """Test de predicción con el modelo"""
    # Primero crear el modelo
    with patch('tabs.linear_model_tab.show_message'):
        linear_model_tab.create_model()
    
    # Mockear los widgets de entrada
    linear_model_tab.prediction_group = MagicMock()
    linear_model_tab.prediction_group.input_widgets = [
        ('x', MagicMock(text=lambda: '2'))
    ]
    
    # Realizar predicción
    with patch('tabs.linear_model_tab.show_error'), \
         patch('tabs.linear_model_tab.show_warning'):
        linear_model_tab.make_prediction()
        
        # Verificar que la predicción es razonable (cerca de 5 según y = 2x + 1)
        predicted_value = float(linear_model_tab.prediction_group.label.setText.call_args[0][0].split('=')[1])
        assert abs(predicted_value - 5) < 1

def test_save_model(linear_model_tab, tmp_path):
    """Test de guardado del modelo"""
    # Primero crear el modelo
    with patch('tabs.linear_model_tab.show_message'):
        linear_model_tab.create_model()
    
    # Crear ruta temporal para el modelo
    model_path = tmp_path / "test_model.joblib"
    
    # Mockear el diálogo de guardado
    with patch('tabs.linear_model_tab.save_file_dialog', return_value=str(model_path)), \
         patch('tabs.linear_model_tab.show_message'):
        # Guardar el modelo
        linear_model_tab.save_model()
        
        # Verificar que el archivo se creó
        assert model_path.exists()
        
        # Cargar el modelo guardado y verificar su contenido
        saved_model = joblib.load(model_path)
        assert "formula" in saved_model
        assert "coefficients" in saved_model
        assert "intercept" in saved_model
        assert "metrics" in saved_model
        assert "columns" in saved_model
        

def test_invalid_prediction_input(linear_model_tab):
    """Test de manejo de entradas inválidas para predicción"""
    # Primero crear el modelo
    with patch('tabs.linear_model_tab.show_message'):
        linear_model_tab.create_model()
    
    # Mockear entrada inválida
    linear_model_tab.prediction_group = MagicMock()
    linear_model_tab.prediction_group.input_widgets = [
        ('x', MagicMock(text=lambda: 'invalid'))
    ]
    
    # Intentar predicción con entrada inválida
    with patch('tabs.linear_model_tab.show_error') as mock_error:
        linear_model_tab.make_prediction()
        mock_error.assert_called_once()