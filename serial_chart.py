from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton
from PyQt5.QtGui import QIcon, QPalette, QColor

class SerialChart(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout() 
        self.setLayout(self.layout)

        self.layout.addWidget(QPushButton("Space"))
