# FirmBench

A professional, extensible Python-based simulator for embedded device firmware development, testing, and protocol analysis. Supports real and virtual sensors, UART communication, and protocol validation—all from a modern CLI shell. Ideal for embedded engineers, firmware developers, and educators.

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Supported Sensors & Connections](#supported-sensors--connections)
- [Setup & Installation](#setup--installation)
- [Configuration (.env)](#configuration-env)
- [Usage](#usage)
- [Example Workflows](#example-workflows)
- [Extending the Simulator](#extending-the-simulator)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

**FirmBench** enables rapid prototyping, testing, and validation of embedded firmware and communication protocols—without requiring full hardware setups. Seamlessly switch between simulated, API-based, or real hardware sensor data. Analyze protocol traffic, validate firmware messages, and automate test flows from the command line.

---

## Architecture

```mermaid
graph TD
    CLI[CLI Shell]
    Device[DeviceSimulator]
    UART[UARTInterface]
    Sensors[SensorReader]
    API[OpenWeatherMap API]
    RealSensor[Real Sensor (UART/I2C/SPI)]
    SimSensor[Simulated Data]

    CLI --> Device
    Device --> UART
    Device --> Sensors
    Sensors --> API
    Sensors --> RealSensor
    Sensors --> SimSensor
```

---

## Features
- **Simulated device registers and sensor data**
- **Real sensor support** (UART, I2C, SPI, GPIO)
- **Open-source API integration** (OpenWeatherMap)
- **Switch sensor modes and API city at runtime**
- **UART communication simulation and logging**
- **Protocol and validation logging**
- **Extensible for new sensor types and protocols**
- **Modern, scriptable CLI shell**

---

## Supported Sensors & Connections
- **DHT22** (GPIO)
- **BMP280** (I2C)
- **SHT31** (I2C)
- **UART/Serial** (custom protocol, e.g., microcontroller)
- **OpenWeatherMap API** (for virtual/remote data)
- **Simulated** (random data)

---

## Setup & Installation

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd Firmware
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

> **Note:** For real sensor support, you may need to install additional libraries:
> - `Adafruit-DHT` (DHT22)
> - `adafruit-circuitpython-bmp280` (BMP280)
> - `adafruit-circuitpython-sht31d` (SHT31)
> - `smbus2`, `pyserial`, `requests`, `python-dotenv`

### 3. Configure `.env`
See [Configuration](#configuration-env) below.

### 4. Run the CLI
```sh
python cli.py
```

---

## Configuration (.env)

Create a `.env` file in the `Firmware/` directory. Example:

```env
# --- Sensor Type and Connection ---
# SENSOR_TYPE: DHT22, BMP280, SHT31, UART, API, SIMULATED
SENSOR_TYPE=API
# SENSOR_CONN: I2C, UART, API, SIMULATED
SENSOR_CONN=API

# --- I2C Settings ---
SENSOR_I2C_ADDR=0x76

# --- SPI Settings (if needed) ---
SENSOR_SPI_BUS=0
SENSOR_SPI_DEVICE=0

# --- UART/Serial Settings ---
SENSOR_UART_PORT=COM3
SENSOR_UART_BAUD=9600

# --- OpenWeatherMap API ---
SENSOR_API_KEY=your_openweathermap_api_key
SENSOR_API_CITY=London

# --- (Optional) GPIO Pin for DHT22 ---
# SENSOR_DHT22_PIN=4
```

---

## Usage

Start the CLI:
```sh
python cli.py
```

### CLI Commands
- `registers` — Show all registers
- `set-register <name> <val>` — Set a register value
- `sensors` — Show sensor data
- `uart-send <data>` — Send data over UART
- `uart-receive` — Receive data from UART
- `log` — Show protocol log
- `validation-log` — Show validation log
- `set-sensor-mode <type>` — Switch sensor type (DHT22, BMP280, SHT31, UART, API, SIMULATED)
- `sensor-status` — Show sensor connection/API status
- `set-api-city <city>` — Set the city for API mode (runtime)
- `help` — Show help
- `exit` — Exit the shell

---

## Example Workflows

### 1. Simulate Sensor Data
```sh
set-sensor-mode SIMULATED
sensors
```

### 2. Use OpenWeatherMap API
```sh
set-sensor-mode API
set-api-city Tokyo
sensors
```

### 3. Connect to a Real Sensor (e.g., UART)
- Set `SENSOR_TYPE=UART` and `SENSOR_CONN=UART` in `.env`
- Set `SENSOR_UART_PORT` and `SENSOR_UART_BAUD` as needed
- In CLI:
```sh
set-sensor-mode UART
sensor-status
sensors
```

### 4. Protocol Analysis
```sh
uart-send CMD:HELLO;
uart-receive
log
validation-log
```

---

## Extending the Simulator
- Add new sensor types by editing `simulator/sensors.py`.
- Add new CLI commands in `cli.py`.
- Extend protocol validation in `device.py`.
- Contributions welcome!

---

## Troubleshooting
- **No sensor data?**
  - Check `.env` settings and sensor connection.
  - For API mode, ensure your API key and city are valid.
- **Import errors for sensor libraries?**
  - Install the required Python packages for your sensor.
- **UART not working?**
  - Check port and baud rate. Ensure no other program is using the port.
- **Still stuck?**
  - Use `sensor-status` and `log` commands for diagnostics.

---

## License

MIT License. See [LICENSE](LICENSE) for details. 