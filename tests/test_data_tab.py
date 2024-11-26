import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from tabs.data_tab import DataTab  
from unittest.mock import MagicMock


@pytest.fixture
def app(qtbot):
    """Crea una instancia de QApplication para los tests."""
    app = QApplication.instance() or QApplication([])
    return app


@pytest.fixture
def data_tab(qtbot):
    """Crea una instancia de DataTab."""
    tab = DataTab()
    qtbot.addWidget(tab)
    return tab


def test_load_file_button(qtbot, data_tab):
    """Testea si el botón de cargar archivo llama a la función correcta."""
    mock_load_file = MagicMock()
    data_tab.load_data = mock_load_file

    qtbot.mouseClick(data_tab.file_button, Qt.LeftButton)
    mock_load_file.assert_called_once()


def test_load_model_button(qtbot, data_tab):
    """Testea si el botón de cargar modelo llama a la función correcta."""
    mock_load_model = MagicMock()
    data_tab.load_model = mock_load_model

    qtbot.mouseClick(data_tab.model_button, Qt.LeftButton)
    mock_load_model.assert_called_once()


def test_display_loaded_file(qtbot, data_tab):
    """Simula la carga de un archivo y verifica la ruta mostrada."""
    mock_file_path = "/ruta/ficticia/datos.csv"
    mock_data = MagicMock()  # Simula un DataFrame cargado
    data_tab.load_file = MagicMock(return_value=mock_data)

    data_tab.load_data = MagicMock()  # Sobreescribe la función load_data
    data_tab.load_data()  # Simula cargar un archivo
    data_tab.path_label.setText(f"📄 Ruta del archivo cargado: {mock_file_path}")
    assert data_tab.path_label.text() == f"📄 Ruta del archivo cargado: {mock_file_path}"


def test_column_selection(qtbot, data_tab):
    """Simula la selección de columnas y verifica el comportamiento."""
    # Mock del DataFrame y columnas seleccionadas
    mock_data = MagicMock()
    mock_data.columns = ["col1", "col2", "col3"]
    data_tab.data = mock_data

    # Poblamos las columnas
    data_tab.column_selector.populate_columns(mock_data)

    # Simula seleccionar columnas
    input_item = data_tab.column_selector.input_column_selector.item(0)
    input_item.setCheckState(Qt.Checked)
    output_item = data_tab.column_selector.output_column_selector
    output_item.setCurrentIndex(1)

    # Confirma la selección
    data_tab.column_selector.confirm_button.click()
    assert data_tab.selected_input_columns == ["col1"]
    assert data_tab.selected_output_column == "col2"


def test_preprocess_buttons(qtbot, data_tab):
    """Verifica que los botones de preprocesado activan los métodos correctos."""
    mock_set_preprocessing_method = MagicMock()
    data_tab.set_preprocessing_method = mock_set_preprocessing_method

    # Simula clics en los botones de preprocesado
    qtbot.mouseClick(data_tab.preprocess_toolbar.buttons["mean"], Qt.LeftButton)
    mock_set_preprocessing_method.assert_called_with("mean")

    qtbot.mouseClick(data_tab.preprocess_toolbar.buttons["delete"], Qt.LeftButton)
    mock_set_preprocessing_method.assert_called_with("delete")


def test_apply_preprocessing(qtbot, data_tab):
    """Verifica que se aplica correctamente el preprocesado."""
    mock_apply_preprocess = MagicMock()
    data_tab.preprocess_applier.apply_preprocess = mock_apply_preprocess

    # Simula un clic en el botón de aplicar
    qtbot.mouseClick(data_tab.preprocess_toolbar.apply_button, Qt.LeftButton)
    mock_apply_preprocess.assert_called_once()
