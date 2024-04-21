import time
import busio
import board
from board import *
import adafruit_scd30
from sparkfun_alphanumeric import QwiicAlphanumeric

while True:
    with busio.I2C(SCL, SDA, frequency=50000) as i2c:
        scd = adafruit_scd30.SCD30(i2c)
        data = scd.data_available
        if data:
            CO2 = scd.CO2
            time.sleep(0.5)
            print(CO2)
    with busio.I2C(SCL, SDA) as i2c:
        display = QwiicAlphanumeric(i2c)
        display.clear()
        display.print(round(CO2, 1))
        time.sleep(0.5)
        
    


