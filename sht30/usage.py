from sht30 import SHT30
import time
sensor = SHT30()
while True:
  temperature, humidity = sensor.measure()

  print('Temperature:', temperature, 'ºC, RH:', humidity, '%') 
