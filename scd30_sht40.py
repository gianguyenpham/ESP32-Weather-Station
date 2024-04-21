import time
import board
import busio
from board import *
import adafruit_scd30
import adafruit_sht4x

while True:
    with busio.I2C(SCL, SDA, frequency=50000) as i2c:
        scd = adafruit_scd30.SCD30(i2c)
        data = scd.data_available
        if data:
            print("CO2:", scd.CO2, "PPM")
    with board.I2C() as i2c:
        sht = adafruit_sht4x.SHT4x(i2c)
        temperature, relative_humidity = sht.measurements
        print("Temperature: %0.1f C" % temperature)
        print("Humidity: %0.1f %%" % relative_humidity)
        time.sleep(1)
        

