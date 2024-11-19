from PyQt5 import QtCore, QtWidgets


class ComboBox(QtWidgets.QComboBox):
    new_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent = None):
        super(ComboBox, self).__init__(parent)
        self.last_selected = 0
        self.current_selection = 0
        self.textActivated.connect(self.on_Activated)

    def on_Activated(self):
        self.last_selected = self.current_selection
        self.current_selection = self.currentIndex()
