import busio
import time
from board import *
from adafruit_bus_device.i2c_device import I2CDevice

def from_bytes(bytes, byteorder='big', signed=False):
    if byteorder == 'little':
        little_ordered = list(bytes)
    elif byteorder == 'big':
        little_ordered = list(reversed(bytes))
    else:
        raise ValueError("byteorder must be either 'little' or 'big'")

    n = sum(b << i*8 for i, b in enumerate(little_ordered))
    if signed and little_ordered and (little_ordered[-1] & 0x80):
        n -= 1 << 8*len(little_ordered)

    return n

BYTES_TO_C = 0.0078125
TS_ADDR = 0X48 #temperature sensor address
TVAL = bytearray([0x0]) #temperature register
bufferIn = bytearray(2)


with busio.I2C(SCL, SDA) as i2c:
    temperatureSensor = I2CDevice(i2c, TS_ADDR)
    with temperatureSensor:
            temperatureSensor.write(TVAL)
    while True:        
        with temperatureSensor:
            temperatureSensor.readinto(bufferIn)
            temperature = from_bytes(bufferIn, "big", True) * BYTES_TO_C
            print(temperature)
            time.sleep(0.1)

    






