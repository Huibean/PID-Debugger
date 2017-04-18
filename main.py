import sys
from PyQt5.QtWidgets import QApplication, QWidget
from main_window import MainWindow

import os

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit([app.exec_(), main_window.close(), os._exit(1)])
