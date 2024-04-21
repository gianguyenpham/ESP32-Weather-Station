# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from board import *
import adafruit_vcnl4040

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