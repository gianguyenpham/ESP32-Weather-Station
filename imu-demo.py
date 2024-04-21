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

###############
## Constants ##
###############
g = 9.80665 #m/s^2
SCALE = 4 * g
BYTES_TO_ACCEL = SCALE/65535

###############
## Addresses ##
###############

IMU_ADDR = 0X6B #imu address
CTRL1_XL = 0x10
CTRL2_G = 0x11
OUTX_L_A = 0x28
OUTY_L_A = 0x2A
OUTZ_L_A = 0x2C

##############

accelCtrl = bytearray([CTRL1_XL, 0xA0])
gyroCtrl = bytearray([CTRL2_G, 0xA0]) 

with busio.I2C(SCL, SDA) as i2c:
    imu = I2CDevice(i2c, IMU_ADDR)
    
    # setting the control registers
    with imu:
            imu.write(accelCtrl)
            imu.write(gyroCtrl)
    
    # reading from output registers
    while True:        
        with imu:
            
            # reading acceleration in Z
            accelZ = bytearray(2)
            imu.write(bytearray([OUTZ_L_A]))
            imu.readinto(accelZ)
            accelZ = from_bytes(accelZ, "little", True) * BYTES_TO_ACCEL
            print(accelZ)
            time.sleep(0.1)

    







