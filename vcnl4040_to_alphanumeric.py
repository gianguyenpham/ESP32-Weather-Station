import time
import busio
import board
from board import *
import adafruit_vcnl4040
from sparkfun_alphanumeric import QwiicAlphanumeric

while True:
    with busio.I2C(SCL, SDA) as i2c:
        sensor = adafruit_vcnl4040.VCNL4040(i2c)
        proximity_value = sensor.proximity
    with busio.I2C(SCL, SDA) as i2c:
        display = QwiicAlphanumeric(i2c)
        display.clear()
        display.print(proximity_value)
        time.sleep(1)
        
    



