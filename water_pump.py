import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json


class WaterPumpModel:
    def __init__(self):
        self.__pin = 23
        GPIO.setup(self.__pin, GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        GPIO.output(self.__pin, GPIO.LOW)
        return {'message': 'start pumping', 'isOn': True}

    def off(self):
        GPIO.output(self.__pin, GPIO.HIGH)
        return {'message': 'stop pumping', 'isOn': False}
    
    
class WaterPump:
    def __init__(self):
        super().__init__()
        self.__water_pump = WaterPumpModel()
        self.__THINGSBOARD_HOST = '192.168.43.142'
        self.__ACCESS_TOKEN = 'IacVgscRF2vHnhSJqXBA'
        self.__client = mqtt.Client()

    def __on_connect(self, client, userdata, rc, *extra_params):
        print('Connected with result code ' + str(rc))
        client.subscribe('v1/devices/me/rpc/request/+')

    def __on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        print(data)
        
        if 'params' in data:
            if data['params']:
                self.__water_pump.on()
            else:
                self.__water_pump.off()
            
    def run(self):
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.username_pw_set(self.__ACCESS_TOKEN)
        self.__client.connect(self.__THINGSBOARD_HOST, 1883, 60)
        self.__client.loop_forever()

    