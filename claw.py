# imports:
import busio
import board
import adafruit_pca9685 as PCA9685
import time

 
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685.PCA9685(i2c, address=0x41)

time.sleep(0.1)

pca.frequency = 200 # hz
actual_frequency = 212.8
#imu channel
channel = 0


def us_to_duty(us : float):
    global actual_frequency
    duty_cycle = us/(1000000/actual_frequency)
    return int(duty_cycle * 65535)


# 0 degrees = 500 us
#360 degrees = 2500 us
def degrees_to_us(degrees: float):
     us = 500.0
     us += 2000/360 * degrees
     return us
     
def degrees_to_duty(degrees: float):
    return us_to_duty(degrees_to_us(degrees))
    
minDuty = degrees_to_duty(0)
# 255 is max for claw
maxDuty = degrees_to_duty(255)

pca.channels[channel].duty_cycle = degrees_to_duty(90)

try:
    for chan in range(16): # there are 16 total, only using 8 here
        pca.channels[chan].duty_cycle = us_to_duty(0.0)
    time.sleep(2.0)
    
    
    while True:
        time.sleep(0.1)
        degrees = float(input("Enter rotation degrees:"))
       
        duty = degrees_to_duty(degrees)
        print("duty0: "+str(duty))
        if minDuty > duty or duty > maxDuty:
            print("out of range")
        else:
            pca.channels[channel].duty_cycle = duty
        

except KeyboardInterrupt:
    pca.channels[channel].duty_cycle = degrees_to_duty(1500)
