from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton, QTextEdit, QComboBox, QFileDialog 
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import QPointF, QTimer, Qt, QMargins

import serial
from serial_status import SerialStatus
from message_manager import MessageManager

from threading import Thread, Event
import re

class LogWindow(QStackedWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.serial_connection = serial.Serial()

        self.serial_data = serialData()

        self.init_unconnect_state_ui()
        self.init_connected_state_ui()
        self.update_ui()

    def start_receive_data(self):
        self.receive_stop = Event()
        self.receive_dataThread = Thread( target = serialData.receive, args = (self.serial_connection, self.serial_data, self.receive_stop))
        self.receive_dataThread.start()

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

    def __init__(self, log_window):
        super().__init__()
        self.log_window = log_window
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
            self.log_window.serial_connection = serial.Serial(device_name, self.selected_baudrate, timeout=0.05)
            print(self.log_window.serial_connection)

            self.log_window.update_ui()
            self.log_window.start_receive_data()
            self.log_window.connected_state_widget.update_data_timer.start(0.5)

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

    def __init__(self, log_window):
        super().__init__()
        self.run = False
        self.log_window = log_window
        self.initUI()
        self.data_index = 0

        self.update_data_timer = QTimer(self)
        self.update_data_timer.timeout.connect(self.update_data)

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.log_text = QTextEdit()

        self.layout.addWidget(self.log_text, 10)

        self.init_button_area()

    def init_button_area(self):
        button_area = QWidget()
        layout = QVBoxLayout()
        button_area.setLayout(layout)
        self.layout.addWidget(button_area, 1)

        self.play_button = QPushButton("绘制")
        self.play_button.clicked.connect(self.toggle_play_button)
        layout.addWidget(self.play_button, 1)

        save_data_button = QPushButton("保存")
        save_data_button.clicked.connect(self.handle_save_data)
        layout.addWidget(save_data_button, 1)

        disconnect_button = QPushButton("断开连接")
        disconnect_button.clicked.connect(self.handle_disconnect)
        layout.addWidget(disconnect_button, 1)


    def toggle_play_button(self):
        if self.run:
            self.log_window.main_window.serial_chart.update_data_timer.stop()
            self.play_button.setText("绘制")
        else:
            self.log_window.main_window.serial_chart.update_data_timer.start(0.1)
            self.play_button.setText("暂停")

        self.run = not self.run

    def handle_save_data(self):
        file_url = QFileDialog.getSaveFileUrl(self, self.tr("保存数据"), "", self.tr("Project Files(*.txt)"))
        project_path = file_url[0].path()
        if (len(project_path) > 0):
            print("保存路径 %s"%project_path)
            try:
                with open(project_path, "w+") as f:
                    f.write(self.log_text.toPlainText())
            except Exception as e:
                raise e
                error_message = "保存失败: " + str(e)
                print(error_message)
                MessageManager(error_message).error()
        else:
            print("用户取消操作")
        
    def update_data(self):
        currentData = self.log_window.serial_data.data
        if len(currentData) >= self.data_index + 1:
            self.log_text.append(", ".join(currentData[self.data_index]))
            self.data_index += 1

    def handle_disconnect(self):
        self.log_window.serial_connection.close()
        self.log_window.update_ui()
        self.log_window.main_window.serial_chart.update_data_timer.stop()
        self.log_window.connected_state_widget.update_data_timer.stop()
        self.log_window.receive_stop.set()

class serialData(object):

    def __init__(self):
        self.data = []
        self.index = 0
        self.buffer = ''

    @staticmethod
    def receive(serial_connection, serial_data, stop_event):
        while (not stop_event.is_set()):
            if serial_connection.isOpen():
                try:
                    serial_data.handle_bytes(serial_connection.read())
                except Exception as e:
                    raise e

    def handle_bytes(self, byte):
        data = byte.decode()
        if re.match('\d|\.|\,|-', data):
            self.buffer += data
        elif re.match('\n|\r', data):
            if len(self.buffer):
                self.data.append(self.buffer.split(","))
                self.index += 1
                self.buffer = ''
        else:
            self.buffer = ''
