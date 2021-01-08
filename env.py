import serial
import Adafruit_DHT
import time
import json
import requests


class Environment:
    def __init__(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 18)
        self.__humidity = humidity
        self.__temperature = temperature
        
        with serial.Serial('/dev/ttyACM0', 9600) as ser:
            soil_moisture = None
            
            while not soil_moisture:
                try:
                    data = ser.readline().decode('utf-8').rstrip()
                    
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
                dht_payload = json.dumps({'temperature': environment.env['temperature'], 'humidity': environment.env['humidity']})
                headers = {'Content-Type': 'application/json'}
                res = requests.post('http://192.168.180.109:8080/api/v1/8vB6QolrAJbsHvPuMPGz/telemetry', headers=headers, data=dht_payload)
                soil_moisture_payload = json.dumps({'percentage': environment.env['soil_moisture']})
                res = requests.post('http://192.168.180.109:8080/api/v1/KtMNWOUG9s6QZZqnu64W/telemetry', headers=headers, data=soil_moisture_payload)
        except KeyboardInterrupt:
            return