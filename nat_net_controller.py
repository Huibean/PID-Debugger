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
        self.positions_track = {}
        self.speed_buffer = {}
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

                    data = CommandTranslator.convert_hex_string(command, controller.positions_buffer, controller.rotations_buffer, controller.speed_buffer)
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

        track_item = [*current_position, datetime.datetime.now()]

        if id in controller.positions_track.keys():
            controller.positions_track[id].append(track_item)
            if len(controller.positions_track[id]) == 11:
                del controller.positions_track[id][0]
                controller.positions_track[id]
                for i in range(3):
                    p1 = controller.positions_track[id][-1]
                    p0 = controller.positions_track[id][0]
                    dtime = p1[3] - p0[3]
                    distance = p1[i] - p0[i]
                    speed = distance / dtime.total_seconds()
                    controller.speed_buffer[id][i] = speed
                print(controller.speed_buffer[id])

        else:
            controller.positions_track[id] = [track_item]
            controller.speed_buffer[id] = [0, 0, 0]

        controller.last_update_buffer_id = id
