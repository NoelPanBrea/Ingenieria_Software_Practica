import sys 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("src/assets/icono.ico"))
    main_win = MainWindow()
    
    main_win.show()
    sys.exit(app.exec_())