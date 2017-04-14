from PyQt5.QtWidgets import QWidget, QComboBox, QListWidget, QListWidgetItem, QStackedWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QAction, QPushButton, QGroupBox, QLabel, QTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox
from PyQt5.QtGui import QIcon, QPalette, QColor

import serial
from serial_status import SerialStatus

class DashBox(QStackedWidget):

    def __init__(self):
        super().__init__()
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

    def handle_active_select(self):
        self.selected_device = self.device_select_box.currentData()
        print("%s selected", self.selected_device)

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
            self.dash_box.serial_connection.write(b"01")
            print(self.dash_box.serial_connection)

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
        self.dash_box = dash_box
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.init_pid_area()
        self.init_aircraft_controll_area()

        self.disconnect_button = QPushButton("断开连接")
        self.layout.addWidget(self.disconnect_button)
        self.disconnect_button.clicked.connect(self.handle_disconnect)

    def handle_disconnect(self):
        self.dash_box.serial_connection.close()
        self.dash_box.update_ui()

    def init_aircraft_controll_area(self):
        self.controll_GroupBox = QGroupBox("控制") 
        layout = QHBoxLayout()

        take_off_button = QPushButton("起飞")
        layout.addWidget(take_off_button)

        landing_button = QPushButton("降落")
        layout.addWidget(landing_button)

        self.controll_GroupBox.setLayout(layout)

        self.layout.addWidget(self.controll_GroupBox, 1, 0)

    def init_pid_area(self):
        self.pid_GroupBox = QGroupBox("PID 调试")
        layout = QGridLayout()
        self.pid_editors = [QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox()]

        layout.addWidget(QLabel("KP: "), 0, 0)
        layout.addWidget(QLabel("KI: "), 1, 0)
        layout.addWidget(QLabel("KD: "), 2, 0)

        self.pid_GroupBox.setLayout(layout)

        for index, editor in enumerate(self.pid_editors):
            layout.addWidget(editor, index, 1)

        send_button = QPushButton("发送")

        layout.addWidget(send_button, 2, 2)

        self.layout.addWidget(self.pid_GroupBox, 0, 0)

