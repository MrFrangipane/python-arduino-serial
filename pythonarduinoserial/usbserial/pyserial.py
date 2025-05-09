import serial
from serial.tools import list_ports

from pythonarduinoserial.usbserial.abstract import AbstractUsbSerial
from pythonarduinoserial.usbserial.exception import UsbSerialException


class PySerialUsbSerial(AbstractUsbSerial):

    def __init__(self):
        self._serial_port = None

    def close(self):
        self._serial_port.close()

    def is_buffer_empty(self) -> bool:
        return self._serial_port.in_waiting == 0

    def list_names(self) -> list[str]:
        return [port.name for port in list_ports.comports()]

    def open(self, name: str):
        self._serial_port = serial.Serial()
        self._serial_port.baudrate = 115200
        self._serial_port.dtr = True
        self._serial_port.port = name
        self._serial_port.timeout = 2
        self._serial_port.write_timeout = 2
        self._serial_port.open()

    def read(self) -> bytearray:
        return self._serial_port.read(self._serial_port.in_waiting)

    def write(self, data: bytearray):
        try:
            self._serial_port.write(data)
            self._serial_port.flush()
        except serial.SerialException as e:
            raise UsbSerialException(e)
