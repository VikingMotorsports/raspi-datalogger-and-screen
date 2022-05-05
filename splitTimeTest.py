import time
from random import randint

lapTime = "00:00:000"
prevLap = "00:00:000"

now = time.time()
prevTime = time.time()

def split():
    global lapTime, prevLap, prevTime, now

    prevLap = lapTime
    lapTime = "00:00:000"

    prevTime = time.time()
    now = time.time()

    

def update():
    global lapTime, prevTime, now

    now = time.time()

    #get base values
    minutes = str(int((now-prevTime)/60))
    seconds = str(int(now-prevTime)%60)
    milliseconds = str(int(((now*1000) - (prevTime*1000))%1000))

    #properly format values so they always take up the same amount of space
    minutes = "0"*(2 - len(minutes)) + minutes 
    seconds = "0"*(2 - len(seconds)) + seconds
    milliseconds = "0"*(3 - len(milliseconds)) + milliseconds

    
    lapTime = minutes + ":" + seconds + ":" + milliseconds

while 1:
    update()
    print(lapTime)
