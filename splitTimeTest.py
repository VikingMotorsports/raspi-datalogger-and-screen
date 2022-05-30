import time
from random import randint

now = time.time()
prevTime = now
lapTime = 0
lapFormatted = "00:00.000"
split = 0;
prevLap = 0;
splitFormatted = "00:00.000"
newLap = False

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

  
#Update the lap time as needed
def update_lap():
    global now, prevTime, newLap, lapTime, prevLap, split, splitFormatted, lapFormatted
    now = time.time()

    if newLap: #Needs to be reworked to work with screen
        lapFormatted = "00:00.000"
        split = lapTime - prevLap
        prevLap = lapTime
        prevTime = now
        newLap = False

    random = randint(1, 100)

    if 1 == random:
        newLap = True

    lapTime = now-prevTime

    lapFormatted = format_time(lapTime)

    if 0 > split:
        splitFormatted = "-" + format_time(abs(split))
    elif 0 < split:
        splitFormatted = "+" + format_time(abs(split))
    else:
        splitFormatted = " " + format_time(abs(split))

while 1:
    update_lap()

    print("Current time: " + lapFormatted
            + " Prev time: " + format_time(prevLap) 
            + " last split: " + splitFormatted);

    time.sleep(0.1)

