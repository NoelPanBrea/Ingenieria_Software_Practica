import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QApplication
from models.description import ModelDescription

@pytest.fixture
def app(qtbot):
    """Crea una instancia de QApplication para pruebas."""
    app = QApplication.instance() or QApplication([])
    return app

@pytest.fixture
def model_description(qtbot):
    """Crea una instancia de ModelDescription para pruebas."""
    model = ModelDescription()
    qtbot.addWidget(model.display_label)  # Agrega el widget al qtbot
    qtbot.addWidget(model.input_field)
    return model

def test_default_text(model_description):
    """Verifica que el texto por defecto sea el esperado."""
    assert model_description.display_label.text() == ModelDescription.DEFAULT_TEXT

def test_update_description(qtbot, model_description):
    """Prueba que actualizar la descripción funcione correctamente."""
    new_description = "Este es un modelo de prueba."
    model_description.input_field.setText(new_description)
    
    # Simula el evento de presionar Enter
    qtbot.keyClick(model_description.input_field, Qt.Key_Return)
    
    assert model_description.get_description() == new_description
    assert model_description.display_label.text() == new_description
    assert not model_description.input_field.isVisible()
    assert model_description.display_label.isVisible()

def test_clear_description(model_description):
    """Prueba que limpiar la descripción funcione correctamente."""
    model_description.set_description("Texto temporal")
    model_description.clear_description()
    assert model_description.get_description() == ""
    assert model_description.display_label.text() == ModelDescription.DEFAULT_TEXT

def test_set_description(model_description):
    """Prueba que establecer una descripción funcione correctamente."""
    description = "Modelo de predicción."
    model_description.set_description(description)
    assert model_description.get_description() == description
    assert model_description.display_label.text() == description

def test_show_edit_mode(qtbot, model_description):
    """Prueba que el modo de edición se active correctamente al hacer clic."""
    model_description.set_description("Descripción existente")
    
    # Simula un clic en el QLabel
    qtbot.mouseClick(model_description.display_label, Qt.LeftButton)
    
    assert model_description.input_field.isVisible()
    assert not model_description.display_label.isVisible()
    assert model_description.input_field.text() == "Descripción existente"

def test_focus_lost(qtbot, model_description):
    """Prueba que al perder el foco, se actualice correctamente."""
    new_description = "Descripción después del enfoque perdido."
    model_description.input_field.setText(new_description)
    
    # Simula pérdida de foco
    qtbot.focusWidget(None)
    
    assert model_description.get_description() == new_description
    assert model_description.display_label.text() == new_description
    assert model_description.display_label.isVisible()
    assert not model_description.input_field.isVisible()

def test_add_to_layout(model_description):
    """Prueba que los widgets se añadan correctamente a un layout."""
    layout = QVBoxLayout()
    model_description.add_to_layout(layout)
    assert model_description.display_label in layout.children()
    assert model_description.input_field in layout.children()
