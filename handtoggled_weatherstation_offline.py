# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import busio
import board
from board import *
import adafruit_sht4x
import adafruit_scd30
import adafruit_veml7700
import adafruit_vcnl4040

Humidity_val = 0
Temperature_val = 0
CO2_val = 0
Lux_val = 0
toggle = "OFF"
Proximity_val = 0
print("Toggle State:", toggle)
while True:
    with busio.I2C(SCL, SDA) as i2c:
        sensor = adafruit_vcnl4040.VCNL4040(i2c)
        Proximity_val = sensor.proximity
        if Proximity_val >= 3:
            if toggle == "OFF":
                toggle = "ON"
            else:
                toggle = "OFF"
            print("Toggle State:", toggle)
            time.sleep(1)
        time.sleep(0.1)
    if toggle == "ON":
        # Poll the message queue
        with busio.I2C(SCL, SDA) as i2c:
            veml7700 = adafruit_veml7700.VEML7700(i2c)
            Lux_val = veml7700.lux        
        with busio.I2C(SCL, SDA) as i2c:
            sht = adafruit_sht4x.SHT4x(i2c)
            Humidity_val = sht.relative_humidity
            Temperature_val = sht.temperature
        with busio.I2C(SCL, SDA, frequency=50000) as i2c:
            scd = adafruit_scd30.SCD30(i2c)
            CO2_val = scd.CO2
            # Send a new message
            print()
            print("Humidity value:",Humidity_val)
            print("Temperature value:",Temperature_val)
            print("CO2 value:",CO2_val)
            print("Lux value:",Lux_val)
            time.sleep(1)