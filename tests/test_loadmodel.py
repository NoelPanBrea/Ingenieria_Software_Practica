"""
Tests para la funcionalidad de carga de modelos.

IMPORTANTE - Orden de ejecución recomendado:
1. test_load_valid_model: Requiere un modelo válido con el siguiente formato:
   {
        "formula": str,
        "coefficients": list,
        "intercept": float,
        "metrics": dict,
        "columns": {
            "input": list,
            "output": str
        },
        "description": str
   }
2. test_load_invalid_model: Prueba con un modelo que no sigue el formato correcto
3. test_load_nonexistent_model: Prueba con un archivo que no existe
"""
import joblib
import sys
import pytest
from src.tabs.data_tab import DataTab
from PyQt5.QtWidgets import QApplication
from pathlib import Path
from unittest.mock import MagicMock, patch

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
def data_tab(qapp):
    """Fixture para el DataTab con mock de componentes críticos"""
    tab = DataTab()
    # Mockear los componentes de UI que pueden causar problemas
    tab.table = MagicMock()
    tab.column_selector = MagicMock()
    tab.preprocess_toolbar = MagicMock()
    return tab

@pytest.fixture
def sample_model():
    """Fixture para crear un modelo de prueba"""
    return {
        "formula": "y = 1.00 + (2.00 * x)",
        "coefficients": [2.0],
        "intercept": 1.0,
        "metrics": {"r2": 0.95},
        "columns": {
            "input": ["x"],
            "output": "y"
        },
        "description": "Test model description"
    }

def test_load_valid_model(data_tab, sample_model, tmp_path):
    """Test que un modelo válido se carga correctamente"""
    # Crear un archivo temporal con el modelo
    model_path = tmp_path / "test_model.joblib"
    joblib.dump(sample_model, model_path)
    
    # Mockear la función de diálogo para evitar la UI real
    with patch('src.ui.popup_handler.open_model_dialog', return_value=str(model_path)):
        # Cargar el modelo
        loaded_model = data_tab.load_model()
        
        # Verificar que el modelo se cargó correctamente
        assert loaded_model is not None
        # Verificar que tiene todos los campos necesarios
        assert "formula" in loaded_model
        assert "coefficients" in loaded_model
        assert "intercept" in loaded_model
        assert "metrics" in loaded_model
        assert "columns" in loaded_model

def test_load_invalid_model(data_tab, tmp_path):
    """Test que un modelo inválido produce un error apropiado"""
    # Crear un archivo temporal con datos inválidos
    invalid_model = {"invalid": "data"}
    model_path = tmp_path / "invalid_model.joblib"
    joblib.dump(invalid_model, model_path)
    
    # Mockear la función de diálogo
    with patch('ui.popup_handler.open_model_dialog', return_value=str(model_path)):
        # Intentar cargar el modelo
        loaded_model = data_tab.load_model()
        # Verificar que la carga falló apropiadamente
        assert loaded_model is None

def test_load_nonexistent_model(data_tab):
    """Test que un archivo inexistente produce un error apropiado"""
    # Mockear la función de diálogo
    with patch('ui.popup_handler.open_model_dialog', return_value="nonexistent_model.joblib"):
        # Intentar cargar el modelo
        loaded_model = data_tab.load_model()
        # Verificar que la carga falló apropiadamente
        assert loaded_model is None