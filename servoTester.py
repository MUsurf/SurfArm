import busio
import board
import adafruit_pca9685 as PCA9685
import time
import calcArmDegrees
import math

 
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685.PCA9685(i2c, address=0x41)

pca.channels[0].duty_cycle = 4880