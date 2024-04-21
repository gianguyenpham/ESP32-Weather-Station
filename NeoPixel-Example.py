import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    pixels.fill(0xADAF00)
    time.sleep(1)
    pixels.fill(0)
    time.sleep(1)