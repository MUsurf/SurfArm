# imports:
import busio
import board
import adafruit_pca9685 as PCA9685
import time
import calcArmDegrees
import math

 
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685.PCA9685(i2c, address=0x41)

time.sleep(0.1)

pca.frequency = 200 # hz
actual_frequency = 212.8
minDuty = 6972
maxDuty = 34864
channel = 0

# duty min: 4873
# duty max: 26649

# 0 degree duty: 500 ms
# 180 degree duty: 2500 ms
def ms_to_duty(ms : float):
    global actual_frequency
    duty_cycle = ms/(1000000/actual_frequency)
    return int(duty_cycle * 65535)


# 0 degrees = 500 ms
#180 degrees = 2500 ms
def degrees_to_ms(degrees: float):
     ms = 500.0
     ms += 2000/180 * degrees
     return ms
     
def degrees_to_duty(degrees: float):
    return ms_to_duty(degrees_to_ms(degrees))
    

pca.channels[channel].duty_cycle = degrees_to_duty(90)

try:
    for chan in range(16): # there are 16 total, only using 8 here
        pca.channels[chan].duty_cycle = ms_to_duty(0.0)
    time.sleep(2.0)
    
    
    while True:
        time.sleep(0.1)
        degrees = float(input("Enter rotation degrees:"))
       
        duty = degrees_to_duty(degrees)
        print("duty0: "+str(duty))
        if minDuty > duty or duty > maxDuty:
            print("out of range")
        else:
            channel = 0
            pca.channels[channel].duty_cycle = duty
        

except KeyboardInterrupt:
    for chan in range(16): # there are 16 total, only using 8 here
        pca.channels[chan].duty_cycle = ms_to_duty(500)
