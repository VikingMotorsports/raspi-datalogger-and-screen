import time
from threading import Thread
from multiprocessing import Process, Pipe
#from screen import start_with_pipe
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

newLap = False
now = time.time()
prevTime = now

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
shiftReg1Data = []
shiftReg2Data = []
accelData = []
adcData = []
timeStamp = "00:00.000"


def run():
    run_screen()
    update_data()

#reads sensors
def data_collect():
    global shiftReg1Data, shiftReg2Data, shiftReg1Len, shiftReg2Len, adcData, accelData, timeStamp
    timeStart = time.time()
    timeElapsed = timeStart
    timeStamp = "00:00.000"
    adcRawData = []
    while 1:
        timeElapsed = time.time() -  timeStart
        timeStamp = format_time(timeElapsed)
        #retrieve data
        accelData = accelHandler.getData()
        adcRawData = adcHandler.getData()
        shiftReg1Data = shiftRegHandler.getData(1, shiftReg1Len)
        shiftReg2Data = shiftRegHandler.getData(2, shiftReg2Len)

        #format data
        for i in range(3):
            for j in range(8):
                adcData.append(str(int(adcRawData[i*8 + j]*100)/100))

#logs data
def data_log():
    global shiftReg1Data, shiftReg2Data, adcData, accelData, timeStamp
    with open('datalog.csv', 'a', encoding='UTF8') as f:
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


#generate dummy data for the screen
def update_data():
    global mph, soc, latG, batStr, tcOn
    while 1:
        for i in range(0,100):
            mph += 1
            soc += 1
            latG += 0.01
            tcOn = True
            batStr = "HOT"

            time.sleep(0.1)

        for i in range(0,100):
            mph -= 1
            soc -= 1
            latG -= 0.01
            tcOn = False
            batStr = "OK"

            time.sleep(0.1)

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
    global now, prevTime, mph, soc, batStr, lapFormatted, splitFormatted, newLap, tcOn, latG
    now = time.time()
    prevTime = now

    while 1:
            connection.send([mph, soc, batStr, lapFormatted, splitFormatted, newLap, tcOn, latG])
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
#    screenDaemon = Process(target=start_with_pipe, args=(screen_conn,), daemon=True) 
#    screenDaemon.start() #start the screen daemon

    #Create the updater daemon thread and pass it the our end of the pipe
#    updaterDaemon =  Thread(target=update_screen, args=(dh_conn,), daemon=True)
#    updaterDaemon.start() #start the updater daemon
     
    #Create a seperate daemon thread to manage collecting data from sensors and input
    dataDaemon = Thread(target=data_collect, daemon=True)
    dataDaemon.start() #start the data daemon

    #Create a seperate daemon thread to manage logging data
    logDaemon = Thread(target=data_log, daemon=True)
    logDaemon.start() #start the log daemon



