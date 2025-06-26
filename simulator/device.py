import os
import threading
import time
import random
import requests
from dotenv import load_dotenv
from simulator.sensors import SensorReader

load_dotenv()

class DeviceSimulator:
    def __init__(self):
        self.registers = {
            'REG0': 0,
            'REG1': 0,
            'REG2': 0
        }
        self.sensors = {
            'temperature': 25.0,
            'humidity': 50.0
        }
        self._lock = threading.Lock()
        self._log = []
        self._validation_log = []
        self._running = True
        self.sensor_reader = SensorReader()
        self._sensor_thread = threading.Thread(target=self._update_sensors, daemon=True)
        self._sensor_thread.start()

    def _check_real_sensor(self):
        # Simulate sensor connection check. Replace with real check if available.
        # For demo, always return False. Implement actual hardware check here.
        return False

    def set_sensor_mode(self, mode):
        with self._lock:
            self.sensor_reader.type = mode.upper()
            return True

    def get_sensor_status(self):
        with self._lock:
            return {
                'type': self.sensor_reader.type,
                'conn': self.sensor_reader.conn
            }

    def _fetch_weather(self):
        if not self.api_key:
            return None, None
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={self.api_city}&appid={self.api_key}&units=metric'
            resp = requests.get(url, timeout=5)
            data = resp.json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            return temp, humidity
        except Exception as e:
            return None, None

    def _read_real_sensor(self):
        # Replace with actual sensor reading code
        # For now, simulate as unavailable
        return None, None

    def _log_event(self, event):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self._log.append({'timestamp': timestamp, **event})
        # Keep log size reasonable
        if len(self._log) > 1000:
            self._log.pop(0)

    def _update_sensors(self):
        while self._running:
            with self._lock:
                temp, humidity = self.sensor_reader.read()
                if temp is not None:
                    self.sensors['temperature'] = temp
                if humidity is not None:
                    self.sensors['humidity'] = humidity
                self._log_event({'type': 'sensor_update', 'sensors': dict(self.sensors), 'mode': self.sensor_reader.type})
            time.sleep(2)

    def get_registers(self):
        with self._lock:
            self._log_event({'type': 'registers_read', 'registers': dict(self.registers)})
            return dict(self.registers)

    def set_register(self, name, value):
        with self._lock:
            if name in self.registers:
                self.registers[name] = value
                self._log_event({'type': 'register_write', 'register': name, 'value': value})
                return True
            return False

    def get_sensors(self):
        with self._lock:
            self._log_event({'type': 'sensors_read', 'sensors': dict(self.sensors)})
            return dict(self.sensors)

    def get_log(self):
        with self._lock:
            return list(self._log)

    def validate_message(self, message):
        valid = isinstance(message, str) and message.startswith('CMD:') and message.endswith(';')
        result = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'message': message,
            'valid': valid
        }
        self._validation_log.append(result)
        # Keep validation log size reasonable
        if len(self._validation_log) > 1000:
            self._validation_log.pop(0)
        self._log_event({'type': 'validation', 'message': message, 'valid': valid})
        return valid

    def get_validation_log(self):
        with self._lock:
            return list(self._validation_log)

    def stop(self):
        self._running = False
        self._sensor_thread.join() 