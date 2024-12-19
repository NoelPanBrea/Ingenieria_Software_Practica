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
        "formula": "y = 2x + 1",
        "coefficients": [2.0],
        "intercept": 1.0,
        "metrics": {"r2": 0.95},
        "columns": ["x", "y"]
    }

def test_load_valid_model(data_tab, sample_model, tmp_path):
    """Test que un modelo válido se carga correctamente"""
    # Crear un archivo temporal con el modelo
    model_path = tmp_path / "test_model.joblib"
    joblib.dump(sample_model, model_path)
    
    # Mockear la función de diálogo para evitar la UI real
    with patch('ui.popup_handler.open_model_dialog', return_value=str(model_path)):
        # Cargar el modelo
        loaded_model = data_tab.load_model()
        
        # Verificar que el modelo se cargó correctamente
        assert loaded_model is not None
        assert loaded_model["formula"] == sample_model["formula"]
        assert loaded_model["coefficients"] == sample_model["coefficients"]
        assert loaded_model["intercept"] == sample_model["intercept"]
        assert loaded_model["metrics"] == sample_model["metrics"]
        assert loaded_model["columns"] == sample_model["columns"]
        
        # Verificar que la UI se actualizó correctamente
        assert "test_model.joblib" in data_tab.path_label.text()

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