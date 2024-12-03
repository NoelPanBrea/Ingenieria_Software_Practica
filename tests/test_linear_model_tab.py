import pytest
import numpy as np
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QLineEdit
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from src.tabs.linear_model_tab import LinearModelTab
from src.models.linear_model import LinearModel

@pytest.fixture
def app():
    """Create a QApplication instance for the tests."""
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array([3, 7, 11])
    return X, y

@pytest.fixture
def linear_model_tab(app, sample_data):
    """Create a LinearModelTab instance with sample data."""
    X, y = sample_data
    tab = LinearModelTab(
        data=X, 
        input_columns=['x1', 'x2'], 
        output_column='y'
    )
    return tab

def test_initialization(linear_model_tab):
    """Test the initialization of LinearModelTab."""
    tab = linear_model_tab
    
    # Check initial attributes
    assert tab.data is not None
    assert tab.input_columns == ['x1', 'x2']
    assert tab.output_column == 'y'
    assert tab.model is None
    assert tab.loaded_model is None

    # Check UI components
    assert hasattr(tab, 'create_model_button')
    assert hasattr(tab, 'formula_label')
    assert hasattr(tab, 'predict_button')
    assert hasattr(tab, 'save_button')
    
def test_create_prediction_inputs(linear_model_tab):
    """Test dynamic creation of prediction input fields."""
    tab = linear_model_tab
    
    # Call method to create input fields
    tab.input_columns = ['x1', 'x2']
    tab.create_prediction_inputs()
    
    # Check input widgets
    assert len(tab.input_widgets) == 2
    assert len(tab.input_columns) == 2
    
    # Verify each widget pair
    for (label, line_edit), column in zip(tab.input_widgets, tab.input_columns):
        assert isinstance(label, QLabel)
        assert isinstance(line_edit, QLineEdit)
        assert label.text() == f"{column}:"

def test_create_model(linear_model_tab, sample_data):
    """Test model creation process."""
    tab = linear_model_tab
    X, y = sample_data
    
    # Create model
    tab.create_model()
    
    # Assertions
    assert tab.model is not None
    assert hasattr(tab.model, 'formula')
    assert hasattr(tab.model, 'coef_')
    assert hasattr(tab.model, 'intercept_')
    
    # UI updates
    assert tab.predict_button.isVisible()
    assert tab.save_button.isVisible()
    assert 'Fórmula del Modelo' in tab.formula_label.text()

def test_make_prediction(linear_model_tab, sample_data):
    """Test prediction functionality."""
    tab = linear_model_tab
    X, y = sample_data
    
    # Create model first
    tab.create_model()
    
    # Set test input values
    for (label, line_edit), value in zip(tab.input_widgets, X[0]):
        line_edit.setText(str(value))
    
    # Simulate prediction
    tab.make_prediction()
    
    # Verify prediction label
    assert tab.prediction_label.isVisible()
    assert tab.prediction_label.text().startswith("Resultado de la predicción")

def test_initialize_from_loaded_model(linear_model_tab):
    """Test loading a pre-trained model."""
    mock_loaded_model = {
        'formula': 'y = 2x1 + 3x2 + 1',
        'columns': {'input': ['x1', 'x2'], 'output': 'y'},
        'coefficients': [2.0, 3.0],
        'intercept': 1.0,
        'metrics': {'r2_score': 0.95, 'rmse': 0.1},
        'description': 'Test model description'
    }
    
    tab = linear_model_tab
    tab.initialize_from_loaded_model(mock_loaded_model)
    
    # Verify model attributes
    assert tab.model is not None
    assert tab.model.formula == 'y = 2x1 + 3x2 + 1'
    assert tab.predict_button.isVisible()
    assert tab.save_button.isVisible()
    
    # Verify label updates
    assert 'y = 2x1 + 3x2 + 1' in tab.formula_label.text()

def test_save_model_without_description(linear_model_tab, monkeypatch):
    """Test saving a model with no description, simulating user interaction."""
    tab = linear_model_tab
    
    # Create model first
    tab.create_model()
    
    # Mock the message box to simulate user clicking 'Yes'
    def mock_exec(self):
        self.clickedButton = lambda: self.addButton("Sí", QMessageBox.YesRole)
    
    monkeypatch.setattr(QMessageBox, 'exec_', mock_exec)
    
    # Simulate saving without description
    with monkeypatch.context() as m:
        m.setattr('tabs.linear_model_tab.save_file_dialog', lambda: '/tmp/test_model.pkl')
        tab.save_model()

def test_clear_previous_graph(linear_model_tab):
    """Test clearing previous graph."""
    tab = linear_model_tab
    
    # Create a mock canvas
    tab.create_model()
    
    # Verify canvas exists
    assert tab.canvas is not None
    
    # Clear graph
    tab.clear_previous_graph()
    
    # Verify canvas is reset
    assert tab.canvas is None

def test_plot_graphs(linear_model_tab):
    """Test graph plotting for 2D and 3D scenarios."""
    tab = linear_model_tab
    
    # Create model
    tab.create_model()
    
    # Check graph generation for single and double input column models
    try:
        if len(tab.model.input_columns) == 1:
            tab.plot2d_graph()
            assert tab.canvas is not None
        elif len(tab.model.input_columns) == 2:
            tab.plot3d_graph()
            assert tab.canvas is not None
    except Exception as e:
        pytest.fail(f"Graph plotting failed: {e}")