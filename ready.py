import shiftRegHandler
import RPi.GPIO as GPIO
import time

preChargeLoc = 0
sdcOkLoc = 1
driveSelectLoc = 2

outputPin = 12
def setup():
    shiftRegHandler.setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(outputPin, GPIO.OUT)
    GPIO.output(outputPin, GPIO.LOW)

def run():
    setup()

    data = []
    pcReady = False
    pcHigh = False
    soReady = False
    dsReady = False
    while 1:
        while not pcReady or not soReady or not dsReady:
            data = shiftRegHandler.getData(1, 8)
            if 1 == data[preChargeLoc]:
                pcReady = False
                pcHigh = True
            elif True == pcHigh:
                pcReady = True
                pcHigh = False

            if 1 == data[sdcOkLoc]:
                soReady = True
            else:
                soReady = False

            if 0 == data[driveSelectLoc]:
                dsReady = True
            else:
                dsReady = False

        GPIO.output(outputPin, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(outputPin, GPIO.LOW)
                
