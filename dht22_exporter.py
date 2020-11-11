#!/usr/bin/env python3

import time
import logging

import Adafruit_DHT
from prometheus_client import start_http_server, Summary, Gauge


logger = logging.getLogger("DHT22_exporter")


SLEEP_TIME = 5
SENSOR = Adafruit_DHT.DHT22
PIN = 4

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

temperature_gauge = Gauge("Temperature", "Current Temperature")
humidity_gauge = Gauge("Humidity", "Current Humidity")

@REQUEST_TIME.time()
def get_values():
    """Read Temp and Humidity from the DHT22 sensor."""
    logger.debug("Quering sensor. Sensor: %s Pin: %s", SENSOR, PIN)
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    logger.info("Got data from the sensor. Temperature: %s, Humidity: %s", temperature, humidity)
    temperature_gauge.set(temperature)
    humidity_gauge.set(humidity)
    logger.debug("Metrics update done. going to sleep for %s seconds", SLEEP_TIME)
    time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)-8s %(message)s')
    start_http_server(8042)
    # collect in loop
    while True:
        get_values()
