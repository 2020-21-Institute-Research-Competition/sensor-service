import time
from datetime import datetime
import RPi.GPIO as GPIO
import requests
import json


class FlowMeter:
    ''' Class representing the flow meter sensor which handles input pulses
        and calculates current flow rate (L/min) measurement
    '''
    
    def __init__(self):
        self.__flow_rate = 0.0
        self.__last_time = datetime.now()
  
    def pulseCallback(self, p):
        ''' Callback that is executed with each pulse 
            received from the sensor 
        '''
       
        # Calculate the time difference since last pulse recieved
        current_time = datetime.now()
        diff = (current_time - self.__last_time).total_seconds()
       
        # Calculate current flow rate
        hertz = 1. / diff
        self.__flow_rate = hertz / 7.5
       
        # Reset time of last pulse
        self.__last_time = current_time
    
    def getFlowRate(self):
        ''' Return the current flow rate measurement. 
            If a pulse has not been received in more than one second, 
            assume that flow has stopped and set flow rate to 0.0
        '''
       
        if (datetime.now() - self.__last_time).total_seconds() > 1:
            self.__flow_rate = 0.0
        
        return self.__flow_rate
  

class WaterFlow:
    def __init__(self):
        super().__init__()
        self.__pin = 24
        
    def run(self):
        ''' Main function for repeatedly collecting flow rate measurements
            and sending them to the SORACOM API
        '''
       
        # Configure GPIO pins
        GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
       
        # Init FlowMeter instance and pulse callback
        flow_meter = FlowMeter()
        GPIO.add_event_detect(self.__pin,
                              GPIO.RISING,
                              callback=flow_meter.pulseCallback,
                              bouncetime=20)
       
        try:
            # Begin infinite loop
            while True:
          
                # Get current timestamp and flow meter reading
                timestamp = str(datetime.now())
                flow_rate = flow_meter.getFlowRate()
                
                try:
                    payload = json.dumps({'volume': flow_rate})
                    headers = {'Content-Type': 'application/json'}
                    requests.post('http://192.168.180.109:8080/api/v1/hMiKvKMoGnbNqrScktaW/telemetry', headers=headers, data=payload)
                except:
                    print('Error while detecting flow rate')
                    continue
                
                # Delay
                time.sleep(5)            
        except KeyboardInterrupt:
            return
