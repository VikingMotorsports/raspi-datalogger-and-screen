import time
from threading import Thread
from multiprocessing import Process, Pipe
from screen import start_with_pipe
from random import randint

#<',=,~~
#   rat to eat bugs

#using global variables is bad practice but its also the easiest way to share data with the updater daemon

mph = 0
bat = 30
coolTemp = 0
batTemp = 3

newLap = False
now = time.time()
prevTime = now
lapTime = "00:00:000"

def run():
    run_screen()
    update_data()

#generate dummy data for the screen
def update_data():
    global mph, bat, coolTemp, batTemp
    while 1:
        for i in range(0,70):
            mph += 1
            bat += 1
            coolTemp += 1
            batTemp += 1

            time.sleep(0.1)

        for i in range(0,70):
            mph -= 1
            bat -= 1
            coolTemp -= 1
            batTemp -= 1

            time.sleep(0.1)
  
#Update the lap time as needed
def update_lap():
    global now, newLap, lapTime, prevTime
    while 1:
        now = time.time()

        if(newLap): #Needs to be reworked to work with screen
            lapTime = "00:00:000"
            prevTime = now
            newLap = False

        #get base values
        minutes = str(int((now-prevTime)/60))
        seconds = str(int(now-prevTime)%60)
        milliseconds = str(int(((now*1000) - (prevTime*1000))%1000))

        #properly format values so they always take up the same amount of space
        minutes = "0"*(2 - len(minutes)) + minutes 
        seconds = "0"*(2 - len(seconds)) + seconds
        milliseconds = "0"*(3 - len(milliseconds)) + milliseconds

        #hook it all up
        lapTime = minutes + ":" + seconds + ":" + milliseconds

#Pass the screen updated info
def update_screen(connection):
    global mph, bat, coolTemp, batTemp, lapTime, newLap
    while 1:
            connection.send([mph, bat, coolTemp, batTemp, lapTime, newLap])
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

    #Create a seperate daemon thread to manage map time
    lapDaemon = Thread(target=update_lap, daemon=True)
    lapDaemon.start() #start the lap daemon


