import sys
sys.path.insert(0, 'src')
from tabs.popup_handler import InputDialog
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = InputDialog(labels=["First","Second","Third","Fourth"])
    if dialog.exec():
        print(dialog.get_inputs())
    exit(0)