import busio
import time
from board import *
from adafruit_bus_device.i2c_device import I2CDevice

bufferOut = bytearray([0x01])
bufferIn = bytearray(2)


with busio.I2C(SCL, SDA) as i2c:
    device = I2CDevice(i2c, 0x0)

    while True:        
        with device:
            device.write(bufferOut)
            time.sleep(0.1)
            device.readinto(bufferIn)
            distance = int.from_bytes(bufferIn, "big") # equivalent to bufferIn[0] << 8 | bufferIn[1]
            print(distance)

    





