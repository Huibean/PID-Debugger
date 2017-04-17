import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.show()
    sys.exit(app.exec_())
