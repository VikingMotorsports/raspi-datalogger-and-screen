import RPi.GPIO as GPIO
import time

pin1 = 3
pin2 = 5
pin3 = 19
pin4 = 23



def setup():#initialize pins
    GPIO.setmode(GPIO.BOARD) #Use physical numbering

    #set up pins to proper
    GPIO.setup(pin1, GPIO.IN)
    GPIO.setup(pin2, GPIO.IN)
    GPIO.setup(pin3, GPIO.IN)
    GPIO.setup(pin4, GPIO.IN)
    #GPIO.setup(testPin, GPIO.IN)

def read(): #read data from chip and print out in command line
    print(str(GPIO.input(pin1)) + ", " + str(GPIO.input(pin2)) + ", " + str(GPIO.input(pin3)) + ", " + str(GPIO.input(pin4)))

def loop():
    while True:
        read()  #get data

setup()
try:
    loop()
except KeyboardInterrupt: #Ctrl c
    GPIO.cleanup()
