import gc
import time
from uos import uname
from machine import Pin
from vl53l0x import VL53L0X
from timeutils import RTC



sensor = VL53L0X()
while True:
  print(sensor.read())
  time.sleep(1)





 
