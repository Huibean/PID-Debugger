import serial
import datetime
from command_translator import CommandTranslator
from angle_convert import AngleConvert
import time

class NatNetController(object):
    frequency = 1000000 * 0.1

    def __init__(self, main_window):
        self.main_window = main_window
        self.send = False
        self.send_time = False
        self.serial = serial.Serial()
        self.positions_buffer = {}
        self.rotations_buffer = {}
        self.command_buffer = []
        self.data = {}

        self.last_send_data_time = datetime.datetime.now()

        self.begin_time = datetime.datetime.now()

        self.last_update_buffer_id = 1

    def handle_buffer(self):
        d_time = datetime.datetime.now() - self.last_send_data_time 
        if d_time.microseconds >= NatNetController.frequency and self.send and self.last_update_buffer_id >= 1 and self.serial.isOpen():
            command = "0000"
            if len(self.command_buffer) > 0:
                command = self.command_buffer[0]
                print("发送命令: ", command)
                del self.command_buffer[0]

            data = CommandTranslator.convert_hex_string(command, self.positions_buffer, self.rotations_buffer)
            self.serial.write(data)
            self.last_send_data_time = datetime.datetime.now()

    @staticmethod
    def store_data(controller, store_data_stop):
        while not store_data_stop.is_set():
            if controller.send:
                for id in controller.positions_buffer.keys():
                    if id in controller.data.keys():
                        controller.data[id].append([*controller.positions_buffer[id], *controller.rotations_buffer[id], datetime.datetime.now().strftime("%H:%M:%S.%f")]) 
                    else:
                        controller.data[id] = []
                time.sleep(0.01)


    @staticmethod
    def frequency_handle_buffer(controller, handle_buffer_stop):
        while not handle_buffer_stop.is_set():
            if controller.send:
                print("handle buffer")
                if controller.serial.isOpen():
                    if not controller.send_time:
                        current_time = datetime.datetime.now()
                        controller.serial.write(CommandTranslator.time_stamp(current_time))
                        controller.send_time = True
                        time.sleep(0.125)
                    
                    command = "0000"
                    if len(controller.command_buffer) > 0:
                        command = controller.command_buffer[0]
                        print("发送命令: ", command)
                        del controller.command_buffer[0]

                    data = CommandTranslator.convert_hex_string(command, controller.positions_buffer, controller.rotations_buffer)
                    controller.serial.write(data)
                time.sleep(0.125)

    @staticmethod
    def receiveNewFrame( frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, latency, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        #  print( "Received frame", frameNumber )
        pass

    @staticmethod
    def receiveRigidBodyFrame( controller, id, position, rotation ):
        #  print( "Received frame for rigid body", id )
        #print( "position: ", position )
        #print( "rotation: ", rotation )
        current_position = position
        current_rotation = AngleConvert.quaternion_to_euler(rotation)
        controller.positions_buffer[id] = current_position
        controller.rotations_buffer[id] = current_rotation
        controller.last_update_buffer_id = id
