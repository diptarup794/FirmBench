import sys
from simulator.device import DeviceSimulator
from simulator.uart import UARTInterface


def print_help():
    print("""
Commands:
  registers                  Show all registers
  set-register <name> <val>  Set register value
  sensors                    Show sensor data
  uart-send <data>           Send data over UART
  uart-receive               Receive data from UART
  log                        Show protocol log
  validation-log             Show validation log
  set-sensor-mode <type>     Switch sensor type (DHT22, BMP280, SHT31, UART, API, SIMULATED)
  sensor-status              Show sensor connection/API status
  set-api-city <city>        Set the city for API mode
  help                       Show this help
  exit                       Exit the shell
""")

def main():
    device = DeviceSimulator()
    uart = UARTInterface(simulated=True)
    print("Embedded Device Simulator CLI Shell. Type 'help' for commands.")
    try:
        while True:
            cmd = input('> ').strip()
            if not cmd:
                continue
            parts = cmd.split()
            if parts[0] == 'registers':
                print(device.get_registers())
            elif parts[0] == 'set-register' and len(parts) == 3:
                name, val = parts[1], parts[2]
                try:
                    val = int(val)
                except ValueError:
                    print('Value must be an integer.')
                    continue
                if device.set_register(name, val):
                    print(f'Register {name} set to {val}')
                else:
                    print(f'Register {name} not found')
            elif parts[0] == 'sensors':
                print(device.get_sensors())
            elif parts[0] == 'uart-send' and len(parts) >= 2:
                data = ' '.join(parts[1:])
                uart.send(data)
                device._log_event({'type': 'uart_send', 'data': data})
                print('UART data sent.')
            elif parts[0] == 'uart-receive':
                data = uart.receive()
                if data is not None:
                    device._log_event({'type': 'uart_receive', 'data': data})
                    valid = device.validate_message(data)
                    print(f'Received: {data} (Valid: {valid})')
                else:
                    print('No data received.')
            elif parts[0] == 'log':
                for entry in device.get_log():
                    print(entry)
            elif parts[0] == 'validation-log':
                for entry in device.get_validation_log():
                    print(entry)
            elif parts[0] == 'set-sensor-mode' and len(parts) == 2:
                mode = parts[1]
                if device.set_sensor_mode(mode):
                    print(f'Sensor mode set to {mode}')
                else:
                    print('Invalid mode. Use "real" or "api".')
            elif parts[0] == 'sensor-status':
                status = device.get_sensor_status()
                print('Sensor status:', status)
            elif parts[0] == 'set-api-city' and len(parts) >= 2:
                city = ' '.join(parts[1:])
                device.sensor_reader.api_city = city
                print(f'API city set to {city}')
            elif parts[0] == 'help':
                print_help()
            elif parts[0] == 'exit':
                break
            else:
                print('Unknown command. Type "help" for a list of commands.')
    finally:
        device.stop()

if __name__ == '__main__':
    main() 