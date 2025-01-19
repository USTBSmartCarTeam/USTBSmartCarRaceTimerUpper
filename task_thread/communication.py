import re
import socket

import serial
from PySide6.QtCore import QThread, Signal


def parse_data(data, pattern_callbacks):
    """
    通用函数，用于匹配指定模式并触发相应的回调。

    :param data: str，要解析的字符串。
    :param pattern_callbacks: list，包含元组，每个元组定义一个模式和回调函数。
                              格式为 [(pattern, callback), ...]。
    """
    for pattern, callback in pattern_callbacks:
        match = re.search(pattern, data)
        if match:
            message = float(match.group(1)) / 1000
            callback(message)


class SerialPortThread(QThread):
    real_received = Signal(float)
    final_received = Signal(float)
    timer_reset = Signal()
    send_status = Signal(str)
    message_received = Signal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.patterns_callbacks = [
            (r"\{([-+]?\d*\.\d+|\d+)\}", self.real_received.emit),
            (r"\[([-+]?\d*\.\d+|\d+)\]", self.final_received.emit),
        ]

        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, bytesize=8, stopbits=serial.STOPBITS_ONE,
                                                   parity=serial.PARITY_NONE, timeout=1)
            self.running = True
        except Exception as e:
            self.send_status.emit(f"打开串口失败：{e}")
            self.running = False
            return

        self.send_status.emit(f"串口打开成功！（绑定端口：{self.port}, 波特率：{self.baudrate}）")

    def run(self):
        try:
            while self.running:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode('ascii', errors='ignore').strip()
                    self.message_received.emit(data)
                    if "Reset" in data:
                        self.timer_reset.emit()
                    else:
                        try:
                            parse_data(data, self.patterns_callbacks)
                        except Exception:
                            continue
        except Exception as e:
            self.stop()
            self.send_status.emit(f"串口连接崩溃: {e}")

    def stop(self):
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()


class TcpServerThread(QThread):
    real_received = Signal(float)
    final_received = Signal(float)
    timer_reset = Signal()
    send_status = Signal(str)

    def __init__(self, host='0.0.0.0', port=32767):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True
        self.clients = []
        self.patterns_callbacks = [
            (r"\{([-+]?\d*\.\d+|\d+)\}", self.real_received.emit),
            (r"\[([-+]?\d*\.\d+|\d+)\]", self.final_received.emit),
        ]

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
            tcp_server.bind((self.host, self.port))
            tcp_server.listen(5)
            tcp_server.settimeout(1.0)

            while self.running:
                try:
                    client_socket, client_address = tcp_server.accept()
                except socket.timeout:
                    continue
                else:
                    with client_socket:
                        self.clients.append(client_socket)
                        while self.running:
                            try:
                                data = client_socket.recv(1024)
                                if not data:
                                    break
                                data = data.decode('ascii', errors='ignore').strip()
                                if "Reset" in data:
                                    self.timer_reset.emit()
                                else:
                                    try:
                                        parse_data(data, self.patterns_callbacks)
                                    except Exception:
                                        continue
                            except ConnectionResetError:
                                break

                        self.clients.remove(client_socket)

    def stop(self):
        self.running = False


class UdpServerThread(QThread):
    real_received = Signal(float)
    final_received = Signal(float)
    timer_reset = Signal()
    send_status = Signal(str)

    def __init__(self, host='0.0.0.0', port=32767):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True
        self.patterns_callbacks = [
            (r"\{([-+]?\d*\.\d+|\d+)\}", self.real_received.emit),
            (r"\[([-+]?\d*\.\d+|\d+)\]", self.final_received.emit),
        ]

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server:
            udp_server.bind((self.host, self.port))

            while True:
                data, _ = udp_server.recvfrom(1024)
                data = data.decode('ascii', errors='ignore').strip()
                print(data)
                if "Reset" in data:
                    self.timer_reset.emit()
                else:
                    try:
                        parse_data(data, self.patterns_callbacks)
                    except Exception:
                        continue

    def stop(self):
        self.running = False
