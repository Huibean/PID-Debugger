import serial
import serial.tools.list_ports
        
class SerialStatus():

    def __init__(self):
        pass

    def serial_ports(self):
        ports = list(serial.tools.list_ports.comports())
        print(ports)

        result = []
        for port_no, description, address in ports:
            try:
                print("checking port %s %s", port_no, description)
                result.append({'port_no': port_no, 'description': description, 'address': address})
            except Exception as e:
                print(e)
        return result

