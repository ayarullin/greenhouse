from flask import Flask, Response
from prometheus_client import Gauge, generate_latest

import busio
import board

from adafruit_htu21d import HTU21D
import adafruit_ads1x15.ads1115 as ads1115
from adafruit_ads1x15.analog_in import AnalogIn

from filelock import FileLock

i2c = busio.I2C(board.SCL, board.SDA)
sensor = HTU21D(i2c)
ads = ads1115.ADS1115(i2c)

content_type = str('text/plain; version=0.0.4; charset=utf-8')

lock = FileLock("/tmp/i2c.lock")

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

current_moisture_pot1 = Gauge(
    'current_moisture_pot1',
    'plnt box one',
    ['room']
)

current_moisture_pot2 = Gauge(
    'current_moisture_pot2',
    'plant box two',
    ['room']
)

current_solar_state = Gauge(
    'current_solar_state',
    'SOLAR',
    ['room']
)


def get_sensors_readings():
    with lock:
        humidity = format(sensor.relative_humidity, ".2f")
        temperature = format(sensor.temperature, ".2f")
        moisture_pot1 = format(AnalogIn(ads, ads1115.P0).value, ".2f")
        moisture_pot2 = format(AnalogIn(ads, ads1115.P1).value, ".2f")
        solar_state = format(AnalogIn(ads, ads1115.P2).value, ".2f")
        response = {
            "temperature": temperature,
            "humidity": humidity,
            "moisture_pot1": moisture_pot1,
            "moisture_pot2": moisture_pot2,
            "solar_state": solar_state
        }
        return response


@app.route('/metrics')
def metrics():
    metrics = get_sensors_readings()
    current_humidity.labels('balcony').set(metrics['humidity'])
    current_temperature.labels('balcony').set(metrics['temperature'])
    current_moisture_pot1.labels('balcony').set(metrics['moisture_pot1'])
    current_moisture_pot2.labels('balcony').set(metrics['moisture_pot2'])
    current_solar_state.labels('balcony').set(metrics['solar_state'])
    return Response(generate_latest(), mimetype=content_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)