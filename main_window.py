from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton
from PyQt5.QtGui import QIcon, QPalette, QColor

from NatNetClient import NatNetClient
from nat_net_controller import NatNetController

from dash_box import DashBox
from log_window import LogWindow
from nat_net_chart import NatNetChart 
from serial_chart import SerialChart

from angle_convert import AngleConvert

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.run = False
        self.initUI()
        self.initNatNet()

    def initUI(self):
        self.setWindowTitle("PID Debugger")
        self.resize(1200, 600)
        self.setMinimumSize(1200, 600)
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnMinimumWidth(0, 600)
        self.layout.setColumnMinimumWidth(1, 600)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowMinimumHeight(0, 150)
        self.layout.setRowMinimumHeight(1, 150)
        self.center_widget = QWidget()
        self.setCentralWidget(self.center_widget)
        self.center_widget.setLayout(self.layout)

        self.initDashBox()
        self.initLogWindow()
        self.initNatNetChart()
        self.initSerialChart()

        self.show()
    
    def initDashBox(self):
        self.dash_box = DashBox(self)
        self.layout.addWidget(self.dash_box, 0, 0)

    def initLogWindow(self):
        self.log_window = LogWindow(self)
        self.layout.addWidget(self.log_window, 1, 0)

    def initNatNetChart(self):
        self.nat_net_chart = NatNetChart(self)
        self.layout.addWidget(self.nat_net_chart, 0, 1)

    def initSerialChart(self):
        self.serial_chart = SerialChart(self.log_window)
        self.layout.addWidget(self.serial_chart, 1, 1)

    def init_play_button(self):
        pass

    def initNatNet(self):
        self.nat_net_controller = NatNetController(self)
        self.nat_net_streaming_client = NatNetClient(self.nat_net_controller)
        self.nat_net_streaming_client.newFrameListener = NatNetController.receiveNewFrame
        self.nat_net_streaming_client.rigidBodyListener = NatNetController.receiveRigidBodyFrame

        self.nat_net_streaming_client.run()

    def close(self):
        print("close nat net client")
        self.nat_net_streaming_client.stop()
        return 0
