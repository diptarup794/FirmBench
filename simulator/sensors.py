import os
import random
import requests

class SensorReader:
    def __init__(self):
        self.type = os.getenv('SENSOR_TYPE', 'API').upper()
        self.conn = os.getenv('SENSOR_CONN', 'API').upper()
        self.api_key = os.getenv('SENSOR_API_KEY')
        self.api_city = os.getenv('SENSOR_API_CITY', 'London')
        self.i2c_addr = int(os.getenv('SENSOR_I2C_ADDR', '0x76'), 16)
        self.spi_bus = int(os.getenv('SENSOR_SPI_BUS', '0'))
        self.spi_device = int(os.getenv('SENSOR_SPI_DEVICE', '0'))
        self.uart_port = os.getenv('SENSOR_UART_PORT', 'COM3')
        self.uart_baud = int(os.getenv('SENSOR_UART_BAUD', '9600'))

    def read(self):
        if self.type == 'DHT22' and self.conn == 'I2C':
            return self._read_dht22_i2c()
        elif self.type == 'BMP280' and self.conn == 'I2C':
            return self._read_bmp280_i2c()
        elif self.type == 'SHT31' and self.conn == 'I2C':
            return self._read_sht31_i2c()
        elif self.type == 'UART':
            return self._read_uart()
        elif self.type == 'API':
            return self._fetch_weather()
        elif self.type == 'SIMULATED':
            return self._read_simulated()
        else:
            return self._read_simulated()

    def _read_dht22_i2c(self):
        try:
            import Adafruit_DHT
            # DHT22 is usually on a GPIO pin, not I2C, but for demo:
            # Replace 4 with your GPIO pin number
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
            return temperature, humidity
        except Exception:
            return None, None

    def _read_bmp280_i2c(self):
        try:
            import board
            import busio
            import adafruit_bmp280
            i2c = busio.I2C(board.SCL, board.SDA)
            bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=self.i2c_addr)
            temperature = bmp280.temperature
            humidity = None  # BMP280 does not provide humidity
            return temperature, humidity
        except Exception:
            return None, None

    def _read_sht31_i2c(self):
        try:
            import board
            import busio
            import adafruit_sht31d
            i2c = busio.I2C(board.SCL, board.SDA)
            sht31 = adafruit_sht31d.SHT31D(i2c, address=self.i2c_addr)
            temperature = sht31.temperature
            humidity = sht31.relative_humidity
            return temperature, humidity
        except Exception:
            return None, None

    def _read_uart(self):
        try:
            import serial
            with serial.Serial(self.uart_port, self.uart_baud, timeout=2) as ser:
                ser.write(b'READ\n')
                line = ser.readline().decode().strip()
                if ',' in line:
                    temp, humidity = map(float, line.split(','))
                    return temp, humidity
        except Exception:
            return None, None

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
        except Exception:
            return None, None

    def _read_simulated(self):
        return round(20 + random.uniform(-5, 5), 2), round(50 + random.uniform(-10, 10), 2) 