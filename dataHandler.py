import time
import math
from threading import Thread
from multiprocessing import Process, Pipe
from screen import start_with_pipe, start_screen
from random import randint
import adcHandler
import shiftRegHandler
import accelHandler
import mount_sd
import csv
import numpy as np
from uartHandler import loop


#<',=,~~
#   rat to eat bugs

#using global variables is bad practice but its also the easiest way to share data with the updater daemon

mph = 0
soc = 0
batStr = "OK"
latG = 1.0
tcOn = False
mark = False
clearLap = False
tcOnVal = 0
pedalPosition = 0
tcThrottle = 0

newLap = False
now = time.time()
prevTime = now

socPot = 0
socMax = 61504
socMin = 512

latPos = 1

batDig = 6

lapDig = 3
markDig = 4
clearDig = 5

lapTime = 0
prevLap = 0
lapFormatted = "00:00.0"

split= 0
splitFormatted = " 00:00.0"

csvHeader = ["TIME ELAPSED", "MARK", "MPH", "SOC", "BATSTATE", "LATG", "NEWLAP", "LAPTIME",
        "TCON", "TCPED", "TCTHROT", "XACCEL", "YACCEL", "ZACCEL", "XGYRO", "YGYRO", "ZGYRO",
        "GPSFIX", "LAT", "LONG", "SATELLITES", "ALT", "SPEED", "ANGLE",
        "POT1", "POT2", "POT3", "POT4", "POT5", "POT6", "POT7", "POT8",
        "Thermistor 1", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 2", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 3", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 4", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 5", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 6", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 7", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 8", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 9", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 10", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 11", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 12", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 13", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 14", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 15", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "Thermistor 16", "Seg 1", "Seg 2", "Seg 3", "Seg 4", "Seg 5", "Seg 6",
        "TS Current", "TS Voltage", "Speed", "State of Charge", "AIR +", "AIR -",
        "PC MC 1", "PC MC 2", "SDC", "BMS OK", "IMD OK", "MC MC1", "MC MC2", "APPS OK", "BSPD OK"]

#shiftReg1Len = 16
#shiftReg1Data = [0 for x in range(shiftReg1Len)]
#shiftReg1Buf = [0 for x in range(shiftReg1Len)]
accelData = [0 for x in range(6)]
adcData = [0 for x in range(8)]
gpsData = [0 for x in range(7)]
tcData = [0 for x in range(4)]
timeStamp = "00:00.0"

page = 0
screenData = "Bababooey"

uartSend = bytes([0,0,0])
uartReceive = [0 for x in range(128)]


def run():
    run_daemons()
    #update_data() TESTING
    generate_dummy_data()


#reads sensors
def data_collect():
    global shiftReg1Data, shiftReg2Data, shiftReg1Len, shiftReg2Len, shiftReg1Buf, shiftReg2Buf, adcData, accelData, timeStamp, tcData
    timeStart = time.time()
    timeElapsed = timeStart
    timeStamp = "00:00.000"
    shiftReg1Raw = []
    shiftReg2Raw = []
    adcRaw = []
    adcRawOld = [0 for x in range(16)]
    while 1:
        timeElapsed = time.time() - timeStart
        timeStamp = format_time(timeElapsed)
        #retrieve data
        try:
            accelData = accelHandler.getData()
        except:
            accelData = ["ERR", "ERR", "ERR", "ERR", "ERR", "ERR"]

        adcRaw = adcHandler.getData()
        for i in range(0, 16):
            adcData[i] = (adcRaw[i] + adcRawOld[i])/2
        adcRawOld = adcRaw

        #Using these extra buffers is a bandaid to filter out random noise caused by what i think is low current when the xserver is running
        shiftReg1Raw = shiftRegHandler.getData(1, shiftReg1Len)
        for i in range(shiftReg1Len):
            if shiftReg1Raw[i] == shiftReg1Buf[i]:
                shiftReg1Data[i] = shiftReg1Buf[i]
            else:
                shiftReg1Buf[i] = shiftReg1Raw[i]


def clear():
    global now, prevTime, clearLap, lapTime, prevLap, split
    prevTime = now
    lapTime = 0
    prevLap = 0
    split = 0
    clearLap = True



#interpret input
def inputs():
    global shiftReg1Data, lapDig, clearDig, markDig, clearLap, mark
    length = 0
    lapDown = False
    clearDown = False
    while 1:
        length = len(shiftReg1Data)
        if lapDig < length:
            if 1 == shiftReg1Data[lapDig]:
                lapDown = True

            if True == lapDown and 0 == shiftReg1Data[lapDig]:
                lapDown = False
                lap()

        if clearDig < length:
            if 1 == shiftReg1Data[clearDig]:
                clearDown = True

            if True == clearDown and 0 == shiftReg1Data[clearDig]:
                clearDown = False
                clear()

        if markDig < length and 1 == shiftReg1Data[markDig]:
            mark = True
        else:
            mark = False

        time.sleep(0.1)


#does uart communication
def uart_exchange(connection):
    global uartSend, uartReceive

    while(1):
        #connection.send(uartSend)
        receive = connection.recv()
        if(len(receive) == 128):
            receive = np.int_(receive)
            receive[112] -= 50
            receive[113] += 150
            uartReceive = receive
            fault_string()
        time.sleep(0.1)


#logs data
def data_log():
    global shiftReg1Data, shiftReg2Data, adcData, accelData, timeStamp, mph, soc, batStr, latG, newLap, tcOn, lapFormatted, mark, pedalPosition, tcThrottle, uartReceive
    while(1):
        try:
            with open('/home/pi/raspi-datalogger-and-screen/datalog.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(csvHeader)
                data = []
                while 1:
                    #coalecse data
                    data = [timeStamp, mark, mph, soc, batStr, latG, newLap, lapFormatted, tcOn, pedalPosition, tcThrottle]
                    data.extend(accelData)
                    data.extend(gpsData)
                    data.extend(adcData)
                    data.extend(uartReceive[:-1])

                    #write to file
                    writer.writerow(data)

                    time.sleep(0.1)
        except:
            print("DATALOGGING ERROR")
            time.sleep(1);

#creates fault display text
def fault_string():
    global uartReceive, screenData
    if(len(uartReceive) == 128):
        screenData = "TS VOLTAGE: " + str(uartReceive[113]) 
        screenData += "\nAIR +: " + str(bool(uartReceive[116]))
        screenData += "\nAIR -: " + str(bool(uartReceive[117]))
        screenData += "\nPC MC 1: " + str(bool(uartReceive[118]))
        screenData += "\nSDC: " + str(bool(uartReceive[120]))
        screenData += "\nBMS OK: " + str(bool(uartReceive[121]))
        screenData += "\nIMD OK: " + str(bool(uartReceive[122]))
        screenData += "\nMC MC 1: " + str(bool(uartReceive[123]))
        screenData += "\nAPPS OK: " + str(bool(uartReceive[124]))
        screenData += "\nBSPD OK: " + str(bool(uartReceive[126]))
        #print(screenData)

#update the data sent to the screen
def update_data():
    global mph, soc, latG, batStr, tcOn, adcData, clearLap, shiftReg1Data, batDig, accelData, mph, pdealPosition, tcThrottle, tcData
    while 1:
        if latPos < len(accelData) and "ERR" != accelData[0]:
            latG = (accelData[latPos]/9.81)
        else:
            latG = "ERR"
        if socPot < len(adcData):
            soc = ((adcData[socPot]-socMin)/(socMax-socMin))*100
            if soc > 100:
                soc = 100
        else:
            soc = 0

        if batDig < len(shiftReg1Data):
            if shiftReg1Data[batDig] == 1:
                batStr = "HOT"
            else:
                batStr = "OK"

        if 4 == len(tcData):
            if 0 == tcData[3]:
                tcOn = False
            else:
                tcOn = True
            mph = tcData[0]
            pedalPosition = tcData[1]
            tcThrottle = tcData[2]
        else:
            tcON = False
            mph = 0;
            pedalPosition = -1;
            tcThrottle = -1;

        time.sleep(0.1)

def average_temps():
    global uartReceive
    sum = 0.0
    for x in range(111):
        if x % 7:
            sum += uartReceive[x]

    return sum/96.0


def generate_dummy_data():
    global mph, soc, latG, batStr, tcOn, adcData, clearLap, shiftReg1Data, batDig, accelData, mph, pdealPosition, tcThrottle, tcData, page, screenData, uartSend, uartReceive

    val = -10
    direction = 1

    while 1:
        if val >= 100 or val < -10:
            direction *= -1

        val += direction*2

        if val > 0:
            latG = (val/9.81)
        else:
            latG = "ERR"
        
        batVal = average_temps()
        if batVal > 45:
            batStr = "HOT"
        else:
            batStr = "OK"

        if val > 50:
            tcOn = False
        else:
            tcOn = True

        if val > 60:
            page = 1
        elif val < 10:
            page = 0

        mph = uartReceive[114]
        soc = uartReceive[115]

        pedalPosition = val
        tcThrottle = val

        time.sleep(0.1)

#Formats time for use in displaying
def format_time(time):
    #get base values
    minutes = str(int((time)/60))
    seconds = str(int(time)%60)
    milliseconds = str(int(((time*10))%10))

    #properly format values so they always take up the same amount of space
    minutes = "0"*(2 - len(minutes)) + minutes
    seconds = "0"*(2 - len(seconds)) + seconds
    milliseconds = "0"*(1 - len(milliseconds)) + milliseconds

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
        splitFormatted = "  00:00.0"
    newLap = True


#Update the lap time as needed
def update_lap():
    global now, newLap, lapTime, prevTime, split, splitFormatted, prevLap, lapFormatted
    now = time.time()

    lapTime = now-prevTime
    lapFormatted = format_time(lapTime)
    if randint(0, 100) == 0:
        lap()


#Pass the screen updated info
def update_screen(connection):
    global now, prevTime, mph, soc, batStr, lapFormatted, splitFormatted, newLap, tcOn, latG, clearLap, page, screenData
    now = time.time()
    prevTime = now

    while 1:
            connection.send([mph, soc, batStr, lapFormatted, splitFormatted, newLap, tcOn, latG, clearLap, page, screenData])
            if True == newLap:
                newLap = False
                lapFormatted = "00:00.0"
            clearLap = False
            update_lap()
            time.sleep(0.1)



#Start the screen
def run_daemons():
    print("Screen")
    screen_conn, dh_conn = Pipe(False) #Open a pipe for the screen
    uart_conn, receive_conn = Pipe(True) #Open a pipe for uart

    #Create the screen daemon and pass it the pipe
    screenDaemon = Process(target=start_with_pipe, args=(screen_conn,), daemon=True)
    screenDaemon.start() #start the screen daemon

    #Create the updater daemon thread and pass it the our end of the pipe
    updaterDaemon =  Thread(target=update_screen, args=(dh_conn,), daemon=True)
    updaterDaemon.start() #start the updater daemon

    #Create a seperate daemon thread to manage collecting data from sensors and input
    #dataDaemon = Thread(target=data_collect, daemon=True)
    #dataDaemon.start() #start the data daemon

    #Create a seperate daemon thread to manage logging data
    logDaemon = Thread(target=data_log, daemon=True)
    logDaemon.start() #start the log daemon

    #Create a sperate daemon thread to manage inputs
#    inputDaemon = Thread(target=inputs, daemon=True)
#    inputDaemon.start() #start the input daemon

    #Create a sperate daemon thread to manage uart communication
    uartDaemon = Thread(target=loop, args=(uart_conn,),  daemon=True)
    uartDaemon.start() # start the uart daemon

    #Create a sperate daemon thread to manage the uart pipe
    receiveDaemon = Thread(target=uart_exchange, args=(receive_conn,),  daemon=True)
    receiveDaemon.start() # start the uart daemon
