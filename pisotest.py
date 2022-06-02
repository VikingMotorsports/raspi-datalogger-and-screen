#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import csv

#define the pins for 74HC165N
dataPin1 = 17 #connect to pin 9 on chip
latchPin1 = 27 #connect to pin 1 on chip
clockPin1 = 22 #connect to pin 2 on chip

dataPin2 = 25 #connect to pin 9 on chip
latchPin2 = 8 #connect to pin 1 on chip
clockPin2 = 7 #connect to pin 2 on chip
prevData1 = [0,0,0,0,0,0,0,0]
prevData2 = [0,0,0,0,0,0,0,0]

def setup():#initialize pins
    
    GPIO.setmode(GPIO.BCM) #Use physical numbering
    #set up pins to proper
    GPIO.setup(dataPin1, GPIO.IN)
    GPIO.setup(clockPin1, GPIO.OUT)
    GPIO.setup(latchPin1, GPIO.OUT)

    GPIO.setup(dataPin2, GPIO.IN)
    GPIO.setup(clockPin2, GPIO.OUT)
    GPIO.setup(latchPin2, GPIO.OUT)

def read(dataPin, latchPin, clockPin): #read data from chip and print out in command line
    data = []
    GPIO.output(latchPin, GPIO.HIGH) #set latch to high so clock inputs aren't ignored
    for i in range(0, 8):
        GPIO.output(clockPin, GPIO.HIGH) #update high on clockpin will shift to next data
        data.append(GPIO.input(dataPin)) #get data
        GPIO.output(clockPin, GPIO.LOW)
    GPIO.output(latchPin, GPIO.LOW) #update low on latchpin will load next set of data
    return data

def printData():
    global prevData1, prevData2, dataPin1, latchPin1, clockPin1, dataPin2, latchPin2, clockPin2
    data1 = read(dataPin1, latchPin1, clockPin1)  #get data
    data2 = read(dataPin2, latchPin2, clockPin2)
    for i in range(8):
        if data1[i] != prevData1[i]:
            prevData1 = data1
            print(prevData1[i], end=" |")
        else:
            print(" ", end= " |")
    print("\t", end=" |")
    for i in range(8):
        if data2[i] != prevData2[i]:
            prevData2 = data2
            print(prevData2[i], end=" |")
        else:
            print(" ", end= " |")
    print()

def logData():
    with open('testlog.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        data = []
        sr1data = []
        sr2data = []
        while 1:
            sr1data = read(dataPin1, latchPin1, clockPin1)  #get data
            sr2data = read(dataPin2, latchPin2, clockPin2)  #get data
            data = []
            data.extend(sr1data)
            data.extend(sr2data)
            writer.writerow(data)
            time.sleep(0.1)

def loop():
    while True:
        printData()

def cleanup():
    GPIO.cleanup()

setup()
if __name__ == "__main__":
    try:
        logData()
    except KeyboardInterrupt: #Ctrl c
        cleanup()
