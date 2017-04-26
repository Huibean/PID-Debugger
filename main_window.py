from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton
from PyQt5.QtGui import QIcon, QPalette, QColor

from NatNetClient import NatNetClient
from nat_net_controller import NatNetController
from threading import Thread, Event

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

    def keyPressEvent(self, event):
        print(event.key())
        key = event.key()
        handlers = {81: [0, 0.1], 87: [1, 0.1], 69: [2, 0.1], 65: [0, -0.1], 83: [1, -0.1], 68: [2, -0.1]}
        handler = handlers[key]
        print(handler)
        editor = self.dash_box.connected_state_widget.pid_editors[handler[0]]
        current_value = editor.value()
        current_value += handler[1]
        editor.setValue(current_value)

        self.dash_box.connected_state_widget.handle_send_pid()
    
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

        self.handle_buffer_stop = Event()
        self.handle_buffer_Thread = Thread( target = NatNetController.frequency_handle_buffer, args = (self.nat_net_controller, self.handle_buffer_stop))
        self.handle_buffer_Thread.start()

        self.store_data_stop = Event()
        self.store_data_Thread = Thread( target = NatNetController.store_data, args = (self.nat_net_controller, self.store_data_stop))
        self.store_data_Thread.start()

    def close(self):
        print("close all threads")
        self.nat_net_streaming_client.stop()
        self.handle_buffer_stop.set()
        self.store_data_stop.set()
        return 0
