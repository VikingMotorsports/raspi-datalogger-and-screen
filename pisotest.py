import RPi.GPIO as GPIO
import time

#define the pins for 74HC165N
dataPin = 11 #connect to pin 9 on chip
dataCompPin = 16 #connect to pin 7 on chip
clockPin = 13 #connect to pin 2 on chip
latchPin = 15 #connect to pin 1 on chip
#testPin = 22 #connects to a button to test whether pins work

value = 0;

def setup():#initialize pins
    GPIO.setmode(GPIO.BOARD) #Use physical numbering

    #set up pins to proper
    GPIO.setup(dataPin, GPIO.IN)
    GPIO.setup(dataCompPin, GPIO.IN)
    GPIO.setup(clockPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    #GPIO.setup(testPin, GPIO.IN)

def read(dataPin, clockPin): #read data from chip and print out in command line
    #print(GPIO.input(testPin))
    GPIO.output(latchPin, GPIO.HIGH) #set latch to high so clock inputs aren't ignored
    for i in range(0, 8):
        GPIO.output(clockPin, GPIO.HIGH) #update high on clockpin will shift to next data
        print("(" + str(GPIO.input(dataPin)) + "," + str(GPIO.input(dataCompPin)) + ")", end = '  ') #get data, ALSO VERY BAD PRINT PRACTICE BUT I DONT CARE
        GPIO.output(clockPin, GPIO.LOW)
    print()
    GPIO.output(latchPin, GPIO.LOW) #update low on latchpin will load next set of data
    

def loop():
    while True:
        read(dataPin, clockPin)  #get data
        time.sleep(0.1)

setup()
try:
    loop()
except KeyboardInterrupt: #Ctrl c
    GPIO.cleanup()
