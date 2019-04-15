#!/usr/bin/env python
 
import RPi.GPIO as GPIO
import time
 
def feed():
    # let the GPIO library know where we've connected our servo to the Pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
 
    try:
        servo = GPIO.PWM(18, 50)
        servo.start(12.5)
 
        # spin left, right, then left again rather than in a continuous circle
        # to prevent the food from jamming the servo
        for index in range(0, 3):
            dutyCycle = 2.5 if (index % 2 == 0) else 12.5
            servo.ChangeDutyCycle(dutyCycle)
            # adjust the sleep time to have the servo spin longer or shorter in that direction
            time.sleep(0.8) 
    finally:
        # always cleanup after ourselves
        servo.stop()
        GPIO.cleanup()
 
if __name__ == '__main__':
    # kick off the feeding process (move the servo)
    feed()