import time
import busio
import board
from board import *
import adafruit_veml7700
from sparkfun_alphanumeric import QwiicAlphanumeric

while True:
    with busio.I2C(SCL, SDA) as i2c:
        veml7700 = adafruit_veml7700.VEML7700(i2c)
        lux_value = veml7700.lux
    with busio.I2C(SCL, SDA) as i2c:
        display = QwiicAlphanumeric(i2c)
        display.clear()
        display.print(round(lux_value))
        
    


