import time
import math
from threading import Thread
from multiprocessing import Process, Pipe
from screen import start_with_pipe, start_screen
from random import randint
import adcHandler
import shiftRegHandler
import accelHandler
import csv

#<',=,~~
#   rat to eat bugs

#using global variables is bad practice but its also the easiest way to share data with the updater daemon

mph = 0
soc = 0
batStr = "OK"
latG = 1.0
tcOn = False
clearLap = False

newLap = False
now = time.time()
prevTime = now

socPot = 0
socMax = 61504
socMin = 512

batDig = 6

lapTime = 0
prevLap = 0
lapFormatted = "00:00.000"

split = 0
splitFormatted = " 00:00.000"

csvHeader = ["TIME ELAPSED", "XACCEL", "YACCEL", "ZACCEL", 
        "POT1", "POT2", "POT3", "POT4", "POT5", "POT6", "POT7", "POT8",
        "POT9", "POT10", "POT11", "POT12", "POT13", "POT14", "POT15", "POTl6",
        "POT17", "POT18", "POT19", "POT20", "POT21", "POT22", "POT23", "POT24",
        "DIG1", "DIG2", "DIG3", "DIG4", "DIG5", "DIG6", "DIG7", "DIG8",
        "DIG9", "DIG10", "DIG11", "DIG12", "DIG13", "DIG14", "DIG15", "DIG16"]

shiftReg1Len = 8
shiftReg2Len = 8
shiftReg1Data = [[0] for x in range(shiftReg1Len)]
shiftReg2Data = [[0] for x in range(shiftReg2Len)]
shiftReg1Buf = [[0] for x in range(shiftReg1Len)]
shiftReg2Buf = [[0] for x in range(shiftReg2Len)]
accelData = []
adcData = []
timeStamp = "00:00.000"


def run():
    run_screen()
    update_data()

#reads sensors
def data_collect():
    global shiftReg1Data, shiftReg2Data, shiftReg1Len, shiftReg2Len, shiftReg1Buf, shiftReg2Buf, adcData, accelData, timeStamp
    timeStart = time.time()
    timeElapsed = timeStart
    timeStamp = "00:00.000"
    #adcRawData = []
    shiftReg1Raw = []
    shiftReg2Raw = []
    while 1:
        timeElapsed = time.time() -  timeStart
        timeStamp = format_time(timeElapsed)
        #retrieve data
        try:
            accelData = accelHandler.getData()
        except:
            accelData = ["ERROR", "ERROR", "ERROR"]

        adcData = adcHandler.getData()

        #Using these extra buffers is a bandaid to filter out random noise caused by what i think is low current when the xserver is running
        shiftReg1Raw = shiftRegHandler.getData(1, shiftReg1Len)
        for i in range(shiftReg1Len):
            if shiftReg1Raw[i] == shiftReg1Buf[i]:
                shiftReg1Data[i] = shiftReg1Buf[i]
            else:
                shiftReg1Buf[i] = shiftReg1Raw[i]

        shiftReg2Raw = shiftRegHandler.getData(2, shiftReg2Len)
        for i in range(shiftReg2Len):
            if shiftReg2Raw[i] == shiftReg2Buf[i]:
                shiftReg2Data[i] = shiftReg2Buf[i]
            else:
                shiftReg2Buf[i] = shiftReg2Raw[i]

        print(str(shiftReg1Data) + "\t" + str(shiftReg2Data))


#logs data
def data_log():
    global shiftReg1Data, shiftReg2Data, adcData, accelData, timeStamp
    with open('/home/vms/raspi-datalogger-and-screen/datalog.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(csvHeader)
        data = []
        while 1:
            #coalecse data 
            data = [timeStamp]
            data.extend(accelData)
            data.extend(adcData)
            data.extend(shiftReg1Data)
            data.extend(shiftReg2Data)
            
            #write to file
            writer.writerow(data)
        
            time.sleep(0.1)

#generate dummy data for the screen
def update_data():
    global mph, soc, latG, batStr, tcOn, adcData, clearLap, shiftReg1Data, batDig
    flip = 1;
    while 1:
        for i in range(0,100):
            mph = str(shiftReg1Data)
            if socPot < len(adcData):
                soc = ((adcData[socPot]-socMin)/(socMax-socMin))*100
                if soc > 100:
                    soc = 100;
            else:
                soc = 0;

            latG += 0.01*flip
            
            if batDig < len(shiftReg1Data):
                if shiftReg1Data[batDig] == 1:
                    batStr = "HOT"
                else:
                    batStr = "OK"
                
            if 1 == flip:
                tcOn = True
            else:
                tcOn = False

            time.sleep(0.1)
        flip *= -1


#Formats time for use in displaying
def format_time(time):
    #get base values
    minutes = str(int((time)/60))
    seconds = str(int(time)%60)
    milliseconds = str(int(((time*1000))%1000))

    #properly format values so they always take up the same amount of space
    minutes = "0"*(2 - len(minutes)) + minutes 
    seconds = "0"*(2 - len(seconds)) + seconds
    milliseconds = "0"*(3 - len(milliseconds)) + milliseconds

    #hook it all up
    formatted = minutes + ":" + seconds + "." + milliseconds
    return formatted

#A function for when the car completes a lap
def lap():
    global now, newLap, lapTime, prevTime, split, splitFormatted, prevLap, lapFormatted

    split = lapTime - prevLap
    prevLap = lapTime
    prevTime = now

    if 0 > split:
        splitFormatted = " -" + format_time(abs(split))
    elif 0 < split:
        splitFormatted = "+" + format_time(abs(split))
    else:
        splitFormatted = "  00:00.000"
    newLap = True

  
#Update the lap time as needed
def update_lap():
    global now, newLap, lapTime, prevTime, split, splitFormatted, prevLap, lapFormatted
    now = time.time()

    random = randint(1, 100)
    lapTime = now-prevTime
    lapFormatted = format_time(lapTime)


    if 1 == random:
        lap()


#Pass the screen updated info
def update_screen(connection):
    global now, prevTime, mph, soc, batStr, lapFormatted, splitFormatted, newLap, tcOn, latG, clearLap
    now = time.time()
    prevTime = now

    while 1:
            connection.send([mph, soc, batStr, lapFormatted, splitFormatted, newLap, tcOn, latG, clearLap])
            if True == newLap:
                newLap = False;
                lapFormatted = "00:00.000"
            update_lap()
            time.sleep(0.1)



#Start the screen
def run_screen():
    print("Screen")
    screen_conn, dh_conn = Pipe(False) #Open a pipe for the screen

    #Create the screen daemon and pass it the pipe
    screenDaemon = Process(target=start_with_pipe, args=(screen_conn,), daemon=True) 
    screenDaemon.start() #start the screen daemon

    #Create the updater daemon thread and pass it the our end of the pipe
    updaterDaemon =  Thread(target=update_screen, args=(dh_conn,), daemon=True)
    updaterDaemon.start() #start the updater daemon
    
    #Create a seperate daemon thread to manage collecting data from sensors and input
    dataDaemon = Thread(target=data_collect, daemon=True)
    dataDaemon.start() #start the data daemon

    #Create a seperate daemon thread to manage logging data
    logDaemon = Thread(target=data_log, daemon=True)
    logDaemon.start() #start the log daemon



