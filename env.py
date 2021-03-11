import serial
import Adafruit_DHT
import time
import json
import requests

from config import post


class Environment:
    def __init__(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 18)
        self.__humidity = humidity
        self.__temperature = temperature
        
        with serial.Serial('/dev/ttyACM0', 9700) as ser:
            soil_moisture = None
            
            while not soil_moisture:
                try:
                    data = ser.read()
                    
                    if data == '':
                        raise Exception('Data not found')
                    
                    soil_moisture = float(data)
                    break
                except:
                    time.sleep(1)
                    
            self.__soil_moisture = soil_moisture

    @property
    def env(self):
        return {
            'temperature': self.__temperature,
            'humidity': self.__humidity,
            'soil_moisture': self.__soil_moisture
        }
    
    
class UpdateEnv:
    def __init__(self):
        super().__init__()
        
    def run(self):
        try:
            while True:
                environment = Environment()
                post('8vB6QolrAJbsHvPuMPGz', {'temperature': environment.env['temperature'], 'humidity': environment.env['humidity']})
                post('KtMNWOUG9s6QZZqnu64W', {'percentage': environment.env['soil_moisture']})
        except KeyboardInterrupt:
            return
