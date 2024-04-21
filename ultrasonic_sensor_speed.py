import busio
import time
from board import *
from adafruit_bus_device.i2c_device import I2CDevice

SLAVE_ADDR = 0x0

bufferOut = bytearray([0x01])
bufferIn = bytearray(2)

v = 0 # mm/s
x1, x2 = 0, 0 # mm
dT = 0.1 #s

with busio.I2C(SCL, SDA) as i2c:
    device = I2CDevice(i2c, SLAVE_ADDR)
    
    while True:
        with device:
            device.write(bufferOut)
            time.sleep(dT)
            device.readinto(bufferIn)
            x2 = int.from_bytes(bufferIn, "big") # equivalent to bufferIn[0] << 8 | bufferIn[1]
            v= (x2 - x1) / dT
            x1 = x2
            print (v)    






