import RPi.GPIO as GPIO
import os
import sys
import signal
import multiprocessing

from env import UpdateEnv
from water_pump import WaterPump
from water_flow import WaterFlow

    
GPIO.setmode(GPIO.BCM)
update_env = multiprocessing.Process(target=UpdateEnv().run)
calculate_water_flow = multiprocessing.Process(target=WaterFlow().run)
pump_water = WaterPump()
    
try:
    update_env.start()
    calculate_water_flow.start()
    pump_water.run()
except:
    update_env.join()
    calculate_water_flow.join()
    GPIO.cleanup()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sys.exit(0)