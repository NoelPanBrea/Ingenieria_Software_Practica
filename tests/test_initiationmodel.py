import pytest
from PyQt5.QtWidgets import QApplication
import sys
from pathlib import Path
from src.tabs.data_tab import DataTab

# Añadir el directorio src al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

@pytest.fixture
def app():
    """Fixture para la aplicación Qt"""
    app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def data_tab(app):
    """Fixture para el DataTab"""
    return DataTab()

@pytest.fixture
def sample_model():
    """Fixture para crear un modelo de prueba"""
    model_data = {
        "formula": "y = 2x + 1",
        "coefficients": [2.0],
        "intercept": 1.0,
        "metrics": {"r2": 0.95},
        "columns": ["x", "y"]
    }
    return model_data

def test_data_tab_initialization(data_tab):
    """Test que la inicialización del DataTab crea todos los componentes necesarios"""
    assert data_tab.data is None
    assert data_tab.selected_input_columns is None
    assert data_tab.selected_output_column is None
    assert hasattr(data_tab, 'preprocess_applier')
    assert hasattr(data_tab, 'file_button')
    assert hasattr(data_tab, 'model_button')
    assert hasattr(data_tab, 'table')
    assert hasattr(data_tab, 'column_selector')
    assert hasattr(data_tab, 'preprocess_label')
    assert hasattr(data_tab, 'preprocess_toolbar')
    
    