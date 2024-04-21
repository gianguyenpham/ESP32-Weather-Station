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
g = 9.80665 # m/s^2
SCALE = 4 * g
BYTES_TO_ACCEL = SCALE / 65535
BYTES_TO_TEMP = 256
###############
## Addresses ##
###############

IMU_ADDR = 0X6B # imu address
CTRL1_XL = 0x10 # acc control register
CTRL2_G = 0x11 # gyro control register
OUTX_L_A = 0x28 # acc output in X
OUTY_L_A = 0x2A # acc output in Y
OUTZ_L_A = 0x2C # acc output in Z

OUT_TEMP_L = 0x20 # temp output 

##############

accelCtrl = bytearray([CTRL1_XL, 0xA0])
gyroCtrl = bytearray([CTRL2_G, 0xA0]) 

# Initialize lists to store accelerometer readings
x_readings = []
y_readings = []
z_readings = []

with busio.I2C(SCL, SDA) as i2c:
    imu = I2CDevice(i2c, IMU_ADDR)
    
    # setting the control registers
    with imu:
            imu.write(accelCtrl)
            imu.write(gyroCtrl)
    
    # reading from output registers
    while True:
        # Reading 10 accelerometer readings for X, Y, and Z axes
        for _ in range(10):
            with imu:
                # Reading acceleration in X, Y, and Z
                accelX = bytearray(2)
                accelY = bytearray(2)
                accelZ = bytearray(2)
                
                imu.write(bytearray([OUTX_L_A]))
                imu.readinto(accelX)
                accelX = from_bytes(accelX, "little", True) * BYTES_TO_ACCEL / g
                
                imu.write(bytearray([OUTY_L_A]))
                imu.readinto(accelY)
                accelY = from_bytes(accelY, "little", True) * BYTES_TO_ACCEL / g
                
                imu.write(bytearray([OUTZ_L_A]))
                imu.readinto(accelZ)
                accelZ = from_bytes(accelZ, "little", True) * BYTES_TO_ACCEL / g
                
                x_readings.append(accelX)
                y_readings.append(accelY)
                z_readings.append(accelZ)
                
                time.sleep(0.1)
        
        # Calculate and print the average of 10 readings for X, Y, and Z axes
        x_average = sum(x_readings) / len(x_readings)
        y_average = sum(y_readings) / len(y_readings)
        z_average = sum(z_readings) / len(z_readings)
        
        print("X average:", x_average, "g")
        print("Y average:", y_average, "g")
        print("Z average:", z_average, "g")
        
        # Clear the lists for the next set of readings
        x_readings.clear()
        y_readings.clear()
        z_readings.clear()
        
        time.sleep(1)  # Wait for 1 second before taking the next set of readings
