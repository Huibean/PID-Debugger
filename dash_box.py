from PyQt5.QtWidgets import QWidget, QComboBox, QListWidget, QListWidgetItem, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton, QGroupBox, QLabel, QTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox, QFileDialog
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSignal

import serial
from serial_status import SerialStatus
from message_manager import MessageManager
from functools import partial
import json
import platform

class DashBox(QStackedWidget):

    command = {'take_off': "0001", "landing": "0002"}

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.serial_connection = serial.Serial()

        self.init_unconnect_state_ui()
        self.init_connected_state_ui()
        self.update_ui()

    def init_unconnect_state_ui(self):
        self.unconnect_state_widget = UnConnectedStateWidget(self)
        self.addWidget(self.unconnect_state_widget)

    def init_connected_state_ui(self):
        self.connected_state_widget = ConnectedStateWidget(self)
        self.addWidget(self.connected_state_widget)

    def update_ui(self):
        if self.serial_connection.isOpen():
            self.setCurrentWidget(self.connected_state_widget)
        else:
            self.setCurrentWidget(self.unconnect_state_widget)

class UnConnectedStateWidget(QWidget):

    def __init__(self, dash_box):
        super().__init__()
        self.dash_box = dash_box
        self.initUI()

        self.load_available_device()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.device_select_box = QComboBox(self)

        self.baudrate_select_box = QComboBox(self)
        self.baudrate_select_box.addItems(['115200', '57600', '56000', '38400', '28800', '19200', '14400', '9600'])

        button_group_widget = QWidget()
        button_group_widget_layout = QHBoxLayout()
        button_group_widget.setLayout(button_group_widget_layout)

        self.connect_button = QPushButton("连接")
        self.connect_button.resize(self.connect_button.sizeHint())
        self.connect_button.clicked.connect(self.handle_connect_device)

        self.re_scan_button = QPushButton("重新扫描")
        self.re_scan_button.resize(self.re_scan_button.sizeHint())
        self.re_scan_button.clicked.connect(self.load_available_device)

        self.layout.addWidget(self.device_select_box)
        self.layout.addWidget(self.baudrate_select_box)

        button_group_widget_layout.addWidget(self.re_scan_button)
        button_group_widget_layout.addWidget(self.connect_button)
        self.layout.addWidget(button_group_widget)

    def handle_connect_device(self):
        self.selected_device = self.device_select_box.currentData()
        self.selected_baudrate = self.baudrate_select_box.currentText()
        device_name = self.selected_device
        try:
            self.dash_box.serial_connection = serial.Serial(device_name, self.selected_baudrate)
            print(self.dash_box.serial_connection)

            self.dash_box.main_window.nat_net_controller.serial = self.dash_box.serial_connection

            self.dash_box.update_ui()

        except Exception as e:
            error_message = "设备连接失败: " + str(e)
            print(error_message)
            MessageManager(error_message).warning()

    def load_available_device(self):
        self.current_available_ports = SerialStatus().serial_ports()
        print("available_ports: %s", self.current_available_ports)
        self.selected_device = self.current_available_ports[0]
        self.device_select_box.clear()
        for port in self.current_available_ports:
            item = port["port_no"] + " | " + port['description']
            self.device_select_box.addItem(item, port["port_no"])

class ConnectedStateWidget(QWidget):

    def __init__(self, dash_box):
        super().__init__()
        self.run = False
        self.dash_box = dash_box
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.init_pid_area()
        self.init_aircraft_controll_area()
        self.init_system_controll_area()

    def handle_disconnect(self):
        self.dash_box.serial_connection.close()
        self.dash_box.main_window.nat_net_controller.send = False
        self.dash_box.main_window.nat_net_chart.update_data_timer.stop()
        self.dash_box.update_ui()
    
    def init_system_controll_area(self):
        self.system_controll_GroupBox = QGroupBox("控制")
        layout = QVBoxLayout()

        self.play_button = QPushButton("发送并绘制")
        layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.toggle_send_location)

        save_data_button = QPushButton("保存")
        save_data_button.clicked.connect(self.handle_save_data)
        layout.addWidget(save_data_button)

        disconnect_button = QPushButton("断开连接")
        layout.addWidget(disconnect_button)
        disconnect_button.clicked.connect(self.handle_disconnect)

        self.system_controll_GroupBox.setLayout(layout)
        self.layout.addWidget(self.system_controll_GroupBox, 0, 2)

    def init_aircraft_controll_area(self):
        self.controll_GroupBox = QGroupBox("Aircraft 控制") 
        layout = QHBoxLayout()

        for item in ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008"]:
            button = QPushButton(item)
            layout.addWidget(button)
            button.clicked.connect(partial(self.handle_command, item))

        self.controll_GroupBox.setLayout(layout)

        self.layout.addWidget(self.controll_GroupBox, 1, 0, 1, 3)

    def handle_save_data(self):
        file_url = QFileDialog.getSaveFileUrl(self, self.tr("保存数据"), "", self.tr("Project Files(*.json)"))
        project_path = file_url[0].path()
        if (len(project_path) > 0):
            print("保存路径 %s"%project_path)
            if platform.system() == 'Darwin':
                path = project_path
            else:
                path = project_path[1:]

            try:
                with open(path, "w+") as f:
                    f.write(json.dumps(self.dash_box.main_window.nat_net_controller.data))

            except Exception as e:
                raise e
                error_message = "保存失败: " + str(e)
                print(error_message)
                MessageManager(error_message).error()
        else:
            print("用户取消操作")

    def toggle_send_location(self):
        if self.run:
            self.dash_box.main_window.nat_net_controller.send = False
            self.dash_box.main_window.nat_net_chart.update_data_timer.stop()
            self.play_button.setText("发送&绘制")
        else:
            self.dash_box.main_window.nat_net_controller.send = True
            self.dash_box.main_window.nat_net_chart.update_data_timer.start(0.1)
            self.play_button.setText("暂停")

        self.run = not self.run

    def handle_command(self, command):
        print("处理指令: ", command)
        self.dash_box.main_window.nat_net_controller.command_buffer.append(command)

    def init_pid_area(self):
        self.pid_GroupBox = QGroupBox("PID 调试")
        layout = QGridLayout()
        self.pid_editors = [CustomSpinBox(), CustomSpinBox(), CustomSpinBox()]

        layout.addWidget(QLabel("KP: "), 0, 0)
        layout.addWidget(QLabel("KI: "), 1, 0)
        layout.addWidget(QLabel("KD: "), 2, 0)

        self.pid_GroupBox.setLayout(layout)

        for index, editor in enumerate(self.pid_editors):
            layout.addWidget(editor, index, 1)

        send_button = QPushButton("发送")
        send_button.clicked.connect(self.handle_send_pid)
        layout.addWidget(send_button, 2, 2)

        self.layout.addWidget(self.pid_GroupBox, 0, 0, 1, 2)

    def handle_send_pid(self):
        pid_values = []
        for editor in self.pid_editors:
            pid_values.append(editor.value() + 10)
        print("发送pid:", pid_values)
        message = PidMessage.convert_data(pid_values)
        self.dash_box.serial_connection.write(message)

    def handle_take_off(self):
        print("起飞")
        self.dash_box.main_window.nat_net_controller.command_buffer.append(DashBox.command['take_off'])

    def handle_landing(self):
        print("降落")
        self.dash_box.main_window.nat_net_controller.command_buffer.append(DashBox.command['landing'])

class CustomSpinBox(QDoubleSpinBox):

    def __init__(self):
        super().__init__()
        self.setDecimals(4)

class PidMessage():
    header = "7e7e"
    footer = "0d0a"

    @staticmethod
    def convert_data(pid_values):
        byte_length = 86
        data = ''
        for value in pid_values:
            data += format(int(value * 10000), "06x")

        pack_data = ''

        for i in range(byte_length * 2 - len(data) - 8):
            pack_data += '0'

        hex_string = PidMessage.header + data + pack_data + PidMessage.footer

        print("发送PID数据: ", hex_string)
        message = bytearray.fromhex(hex_string)
        print("字节长: ", len(message))
        return message
