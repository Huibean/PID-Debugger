from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QAction, QPushButton
from PyQt5.QtGui import QIcon, QPalette, QColor

from NatNetClient import NatNetClient

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initNatNet()

    def initUI(self):
        self.show()

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
