import time
import busio
import board
from board import *
import adafruit_sht4x
from sparkfun_alphanumeric import QwiicAlphanumeric

while True:
    with busio.I2C(SCL, SDA) as i2c:
        sht = adafruit_sht4x.SHT4x(i2c)
        temperature, relative_humidity = sht.measurements
    with busio.I2C(SCL, SDA) as i2c:
        display = QwiicAlphanumeric(i2c)
        display.clear()
        display.print(round(relative_humidity, 2))
        
    

