import RPi.GPIO as GPIO
import time

#define the pins for 74HC165N
dataPin1 = 17 #connect to pin 9 on chip
latchPin1 = 27 #connect to pin 1 on chip
clockPin1 = 22 #connect to pin 2 on chip

dataPin2 = 25 #connect to pin 9 on chip
latchPin2 = 8 #connect to pin 1 on chip
clockPin2 = 7 #connect to pin 2 on chip

def setup():#initialize pins
    
    GPIO.setmode(GPIO.BCM) #Use physical numbering
    #set up pins to proper
    GPIO.setup(dataPin1, GPIO.IN)
    GPIO.setup(clockPin1, GPIO.OUT)
    GPIO.setup(latchPin1, GPIO.OUT)

    GPIO.setup(dataPin2, GPIO.IN)
    GPIO.setup(clockPin2, GPIO.OUT)
    GPIO.setup(latchPin2, GPIO.OUT)

def read(dataPin, latchPin, clockPin, amount): #read data from chip and print out in command line
    data = []
    GPIO.output(latchPin, GPIO.HIGH) #set latch to high so clock inputs aren't ignored
    for i in range(0, amount):
        GPIO.output(clockPin, GPIO.HIGH) #update high on clockpin will shift to next data
        data.append(GPIO.input(dataPin)) #get data
        GPIO.output(clockPin, GPIO.LOW)
    GPIO.output(latchPin, GPIO.LOW) #update low on latchpin will load next set of data
    return data;

def printData():
    print("\nShift regs")
    print(read(dataPin1, latchPin1, clockPin1, 8))  #get data
    print(end = '\t')
    print(read(dataPin2, latchPin2, clockPin2, 8))
    print()

#returns the data from the shift regs
def getData(reg, amount):
    if 1 == reg:
        return read(dataPin1, latchPin1, clockPin1, amount)
    elif 2 == reg:
        return read(dataPin2, latchPin2, clockPin2, amount)
    return -1;


def loop():
    while True:
        printData()
        time.sleep(0.1)

def cleanup():
    GPIO.cleanup()

setup()
if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt: #Ctrl c
        cleanup()
