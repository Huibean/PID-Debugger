from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton
from PyQt5.QtGui import QIcon, QPalette, QColor

class NatNetChart(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QPushButton("XXXX"))
