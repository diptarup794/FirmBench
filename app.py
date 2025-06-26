from flask import Flask, render_template_string, jsonify, request, render_template
from simulator.device import DeviceSimulator
from simulator.uart import UARTInterface

app = Flask(__name__)
device = DeviceSimulator()
uart = UARTInterface(simulated=True)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api/registers', methods=['GET', 'POST'])
def api_registers():
    if request.method == 'GET':
        return jsonify(device.get_registers())
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        value = data.get('value')
        if name is None or value is None:
            return jsonify({'error': 'Missing name or value'}), 400
        success = device.set_register(name, value)
        if success:
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'error': 'Register not found'}), 404

@app.route('/api/sensors', methods=['GET'])
def api_sensors():
    return jsonify(device.get_sensors())

@app.route('/api/log', methods=['GET'])
def api_log():
    return jsonify(device.get_log())

@app.route('/log')
def log_view():
    log = device.get_log()
    table = '<table border="1"><tr><th>Timestamp</th><th>Type</th><th>Details</th></tr>'
    for entry in log[::-1]:
        details = {k: v for k, v in entry.items() if k not in ('timestamp', 'type')}
        table += f"<tr><td>{entry['timestamp']}</td><td>{entry.get('type','')}</td><td>{details}</td></tr>"
    table += '</table>'
    return render_template_string('<h1>Protocol Log</h1>' + table)

@app.route('/api/uart/send', methods=['POST'])
def uart_send():
    data = request.get_json().get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    uart.send(data)
    device._log_event({'type': 'uart_send', 'data': data})
    return jsonify({'status': 'sent'})

@app.route('/api/uart/receive', methods=['GET'])
def uart_receive():
    received = uart.receive()
    if received is not None:
        device._log_event({'type': 'uart_receive', 'data': received})
        valid = device.validate_message(received)
        return jsonify({'data': received, 'valid': valid})
    else:
        return jsonify({'data': None})

@app.route('/api/validation_log', methods=['GET'])
def api_validation_log():
    return jsonify(device.get_validation_log())

@app.route('/validation_log')
def validation_log_view():
    log = device.get_validation_log()
    table = '<table border="1"><tr><th>Timestamp</th><th>Message</th><th>Valid</th></tr>'
    for entry in log[::-1]:
        table += f"<tr><td>{entry['timestamp']}</td><td>{entry['message']}</td><td>{'Yes' if entry['valid'] else 'No'}</td></tr>"
    table += '</table>'
    return render_template_string('<h1>Validation Log</h1>' + table)

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        device.stop() 