import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QListWidgetItem
import pandas as pd
import joblib
from src.tabs.data_tab import DataTab

@pytest.fixture
def app():
    """Create a QApplication instance for the tests."""
    app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def data_tab(app):
    """Create a DataTab instance for testing."""
    return DataTab()

def test_initialization(data_tab):
    """Test the initialization of DataTab."""
    assert data_tab.data is None
    assert data_tab.selected_input_columns is None
    assert data_tab.selected_output_column is None
    assert hasattr(data_tab, 'load_button')
    assert hasattr(data_tab, 'table')
    assert hasattr(data_tab, 'column_selector')

@patch('ui.popup_handler.open_file_dialog')
def test_load_data_successful(mock_open_dialog, data_tab, mocker):
    """Test successful data loading."""
    # Mock the file dialog to return a test file path
    mock_open_dialog.return_value = 'test_data.csv'
    
    # Mock the load_file function
    mock_load_file = mocker.patch('data_processing.import_module.load_file')
    mock_dataframe = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_load_file.return_value = mock_dataframe
    
    # Call the load_data method
    data_tab.load_data()
    
    # Assertions
    assert data_tab.data is not None
    assert data_tab.path_label.text().startswith('📄 Ruta del archivo cargado:')
    assert data_tab.column_selector.isVisible()

@patch('ui.popup_handler.open_model_dialog')
def test_load_model_successful(mock_open_model_dialog, data_tab):
    """Test successful model loading."""
    # Prepare a mock model data
    mock_model_data = {
        'formula': 'y = 2x + 1',
        'coefficients': [2],
        'intercept': 1,
        'metrics': {'r2': 0.9},
        'columns': {'input': ['x'], 'output': 'y'}
    }
    
    # Mock joblib and file dialog
    with patch('joblib.load', return_value=mock_model_data) as mock_joblib_load:
        mock_open_model_dialog.return_value = '/path/to/model.pkl'
        
        # Call load_model
        loaded_model = data_tab.load_model()
        
        # Assertions
        assert loaded_model is not None
        assert loaded_model == mock_model_data
        assert data_tab.path_label.text().startswith('📄 Ruta del modelo cargado:')

def test_on_input_column_selection_changed(data_tab, mocker):
    """Test input column selection change."""
    # Create a mock QListWidgetItem
    mock_item = MagicMock()
    mock_item.checkState.return_value = 1  # Checked state
    
    # Mock the column selector and table
    mocker.patch.object(data_tab.column_selector.input_column_selector, 'row', return_value=1)
    mock_highlight = mocker.patch.object(data_tab.table, 'highlight_column')
    
    # Simulate output column selection
    mocker.patch.object(data_tab.column_selector.output_column_selector, 'currentIndex', return_value=0)
    
    # Call the method
    data_tab.on_input_column_selection_changed(mock_item)
    
    # Assert column was highlighted
    mock_highlight.assert_called_once()

def test_on_selection_confirmed_no_input_columns(data_tab, mocker):
    """Test column selection confirmation with no input columns."""
    # Mock column selector to return empty input columns
    mocker.patch.object(data_tab.column_selector, 'get_selected_columns', 
                        return_value=([], 'output_col'))
    
    # Mock show_error
    mock_show_error = mocker.patch('ui.popup_handler.show_error')
    
    # Call the method
    data_tab.on_selection_confirmed()
    
    # Assert error was shown
    mock_show_error.assert_called_once()

def test_set_preprocessing_method(data_tab):
    """Test setting preprocessing method."""
    data_tab.set_preprocessing_method('mean')
    
    # Check that the method was set in the preprocess_applier
    assert data_tab.preprocess_applier.current_method == 'mean'

def test_handle_constant_method(data_tab, mocker):
    """Test handling constant preprocessing method."""
    # Set some selected input columns
    data_tab.selected_input_columns = ['col1', 'col2']
    data_tab.selected_output_column = 'output'
    
    # Mock the InputDialog
    mock_input_dialog = MagicMock()
    mock_input_dialog.get_inputs.return_value = {'col1': 0, 'col2': 1, 'output': 2}
    
    # Patch the InputDialog creation
    with patch('ui.popup_handler.InputDialog', return_value=mock_input_dialog) as mock_dialog:
        # Call the method
        data_tab.handle_constant_method()
        
        # Assertions
        mock_dialog.assert_called_once()
        assert data_tab.preprocess_applier.current_method == 'constant'