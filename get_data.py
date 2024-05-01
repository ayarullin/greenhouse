import time
from flask import Flask, Response
from prometheus_client import Counter, Gauge, start_http_server, generate_latest

import busio
import board

from adafruit_htu21d import HTU21D

i2c = busio.I2C(board.SCL, board.SDA)
sensor = HTU21D(i2c)

content_type = str('text/plain; version=0.0.4; charset=utf-8')

app = Flask(__name__)

current_humidity = Gauge(
    'current_humidity',
    'the current humidity percentage, this is a gauge as the value can increase or decrease',
    ['room']
)

current_temperature = Gauge(
    'current_temperature',
    'the current temperature in celsius, this is a gauge as the value can increase or decrease',
    ['room']
)


def get_sensors_readings():
    humidity = format(sensor.relative_humidity, ".2f")
    temperature = format(sensor.temperature, ".2f")
    response = {"temperature": temperature, "humidity": humidity}
    return response


@app.route('/metrics')
def metrics():
    metrics = get_sensors_readings()
    current_humidity.labels('balcony').set(metrics['humidity'])
    current_temperature.labels('balcony').set(metrics['temperature'])
    return Response(generate_latest(), mimetype=content_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
