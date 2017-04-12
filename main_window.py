from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton
from PyQt5.QtGui import QIcon, QPalette, QColor

from NatNetClient import NatNetClient

from dash_box import DashBox
from log_window import LogWindow
from nat_net_chart import NatNetChart 
from serial_chart import SerialChart

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initNatNet()

    def initUI(self):
        #  self.setGeometry(50, 50, 100, 100)
        self.setWindowTitle("PID Debugger")
        self.resize(1000, 600)
        self.setMinimumSize(1000, 600)
        self.layout = QGridLayout() 
        self.center_widget = QWidget()
        self.setCentralWidget(self.center_widget)
        self.center_widget.setLayout(self.layout)

        self.initDashBox()
        self.initLogWindow()
        self.initNatNetChart()
        self.initSerialChart()

        self.show()
    
    def initDashBox(self):
        self.dash_box = DashBox()
        self.layout.addWidget(self.dash_box, 0, 0)

    def initLogWindow(self):
        self.log_window = LogWindow()
        self.layout.addWidget(self.log_window, 1, 0)

    def initNatNetChart(self):
        self.nat_net_chart = NatNetChart()
        self.layout.addWidget(self.nat_net_chart, 0, 1)

    def initSerialChart(self):
        self.serial_chart = SerialChart()
        self.layout.addWidget(self.serial_chart, 1, 1)

    def initNatNet(self):
        self.nat_net_controller = NatNetController()
        self.nat_net_streaming_client = NatNetClient(self.nat_net_controller)
        self.nat_net_streaming_client.newFrameListener = NatNetController.receiveNewFrame
        self.nat_net_streaming_client.rigidBodyListener = NatNetController.receiveRigidBodyFrame

        self.nat_net_streaming_client.run()

class NatNetController(object):

    def __init__(self):
        pass

    @staticmethod
    def receiveNewFrame( frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, latency, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        print( "Received frame", frameNumber )

    @staticmethod
    def receiveRigidBodyFrame( controller, id, position, rotation ):
        print( "Received frame for rigid body", id )
        print( "position: ", position )
        print( "rotation: ", rotation )

        serial_connection.positions_buffer[id] = position
        serial_connection.last_update_buffer_id = id
        serial_connection.handle_position_buffer()
