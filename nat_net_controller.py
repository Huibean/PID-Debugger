import serial
import datetime
from command_translator import CommandTranslator
from angle_convert import AngleConvert

class NatNetController(object):
    frequency = 1000000 * 0.1

    def __init__(self, main_window):
        self.main_window = main_window
        self.serial = serial.Serial()
        self.positions_buffer = {}
        self.rotations_buffer = {}

        self.last_send_data_time = datetime.datetime.now()

        self.begin_time = datetime.datetime.now()

        self.last_update_buffer_id = 1

    def handle_buffer(self):
        d_time = datetime.datetime.now() - self.last_send_data_time 
        if d_time.microseconds >= NatNetController.frequency and self.last_update_buffer_id >= 1 and self.serial.isOpen():
            data = CommandTranslator.convert_hex_string("0000", self.positions_buffer, self.rotations_buffer)
            self.serial.write(data)
            self.last_send_data_time = datetime.datetime.now()

    @staticmethod
    def receiveNewFrame( frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, latency, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        #  print( "Received frame", frameNumber )
        pass

    @staticmethod
    def receiveRigidBodyFrame( controller, id, position, rotation ):
        #  print( "Received frame for rigid body", id )
        #  print( "position: ", position )
        #  print( "rotation: ", rotation )
        #  result = AngleConvert.quaternion_to_euler(rotation)
        #  print(result)

        controller.positions_buffer[id] = position
        controller.rotations_buffer[id] = rotation
        controller.last_update_buffer_id = id
        controller.handle_buffer()
