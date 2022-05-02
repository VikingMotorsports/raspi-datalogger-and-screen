import time
from threading import Thread
from multiprocessing import Process, Pipe
from screen import start_with_pipe

#<',=,~~
#   rat to eat bugs

#using global variables is bad practice but its also the easiest way to share data with the updater daemon

mph = 0
bat = 30
coolTemp = 0
batTemp = 3

def run():
    run_screen()
    update_data()

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
    

#Pass the screen updated info
def update_screen(connection):
    global mph, bat, coolTemp, batTemp
    while 1:
            connection.send([mph, bat, coolTemp, batTemp])
            time.sleep(0.1)



#Start the screen
def run_screen():
    print("Screen")
    screen_conn, dh_conn = Pipe(False) #Open a pipe for the screen

    #Create the screen daemon and pass it the pipe
    screenDaemon = Process(target=start_with_pipe, args=(screen_conn,), daemon=True) 
    screenDaemon.start() #start the screen daemon

    #Create the updater daemon and pass it the our end of the pipe
    updaterDaemon =  Thread(target=update_screen, args=(dh_conn,), daemon=True)
    updaterDaemon.start() #start the updater daemon

