import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

