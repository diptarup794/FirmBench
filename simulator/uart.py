import threading
import queue
try:
    import serial
except ImportError:
    serial = None

class UARTInterface:
    def __init__(self, simulated=True, port=None, baudrate=9600):
        self.simulated = simulated
        self.port = port
        self.baudrate = baudrate
        if simulated:
            self._rx_queue = queue.Queue()
            self._tx_queue = queue.Queue()
        else:
            if serial is None:
                raise ImportError('pyserial is required for real UART mode')
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
        self._lock = threading.Lock()

    def send(self, data):
        with self._lock:
            if self.simulated:
                # Loopback: sent data is immediately available to receive
                self._rx_queue.put(data)
                self._tx_queue.put(data)
            else:
                self.ser.write(data.encode() if isinstance(data, str) else data)

    def receive(self):
        with self._lock:
            if self.simulated:
                try:
                    return self._rx_queue.get_nowait()
                except queue.Empty:
                    return None
            else:
                if self.ser.in_waiting:
                    return self.ser.read(self.ser.in_waiting)
                return None

    def set_mode(self, simulated, port=None, baudrate=9600):
        with self._lock:
            self.simulated = simulated
            if simulated:
                self._rx_queue = queue.Queue()
                self._tx_queue = queue.Queue()
                if hasattr(self, 'ser'):
                    self.ser.close()
                    del self.ser
            else:
                if serial is None:
                    raise ImportError('pyserial is required for real UART mode')
                self.ser = serial.Serial(port, baudrate, timeout=0.1)
                self.port = port
                self.baudrate = baudrate 