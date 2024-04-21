import busio
import time
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
from sparkfun_alphanumeric import QwiicAlphanumeric

bufferOut = bytearray([0x01])
bufferIn = bytearray(2)

distance = 0

while True:
    with busio.I2C(SCL, SDA) as i2c:
        device = I2CDevice(i2c, 0x0)
        with device:
            device.write(bufferOut)
            time.sleep(1)
            device.readinto(bufferIn)
            distance = int.from_bytes(bufferIn, "big") # equivalent to bufferIn[0] << 8 | bufferIn[1]
    with busio.I2C(SCL, SDA) as i2c:
        display = QwiicAlphanumeric(i2c)
        display.clear()
        display.print(round(distance/10, 2))