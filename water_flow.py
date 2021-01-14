import time
from datetime import datetime
import RPi.GPIO as GPIO
import json

from config import post


class FlowMeter:
    def __init__(self):
        self.__flow_rate = 0.0
        self.__last_time = datetime.now()
  
    def pulseCallback(self, p):
        current_time = datetime.now()
        diff = (current_time - self.__last_time).total_seconds()
       
        hertz = 1. / diff
        self.__flow_rate = hertz / 7.5
       
        self.__last_time = current_time
    
    def getFlowRate(self):
        if (datetime.now() - self.__last_time).total_seconds() > 1:
            self.__flow_rate = 0.0
        
        return self.__flow_rate
  

class WaterFlow:
    def __init__(self):
        super().__init__()
        self.__pin = 24
        
    def run(self):
        GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
       
        flow_meter = FlowMeter()
        GPIO.add_event_detect(self.__pin,
                              GPIO.RISING,
                              callback=flow_meter.pulseCallback,
                              bouncetime=20)
       
        try:
            while True:
                timestamp = str(datetime.now())
                flow_rate = flow_meter.getFlowRate()
                
                try:
                    post('hMiKvKMoGnbNqrScktaW', {'volume': flow_rate})
                except:
                    print('Error while detecting flow rate')
                    continue
                
                time.sleep(5)            
        except KeyboardInterrupt:
            return
