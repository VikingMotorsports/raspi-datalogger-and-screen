import time
from threading import Thread
from multiprocessing import Process, Pipe
from screen import start_screen

#<',=,~~
#   rat to eat bugs

def run():
    run_screen()
    

#Pass the screen updated info
def update_screen(connection):
    mph = 0
    bat = 30
    coolTemp = 0
    batTemp = 3
    motTemp = 6

    while 1:

        for i in range(0,70):
            mph += 1
            bat += 1
            coolTemp += 1
            batTemp += 1
            motTemp += 1

            connection.send([mph, bat, coolTemp, batTemp, motTemp])
            time.sleep(0.1)

        for i in range(0,70):
            mph -= 1
            bat -= 1
            coolTemp -= 1
            batTemp -= 1
            motTemp -= 1

            connection.send([mph, bat, coolTemp, batTemp, motTemp])
            time.sleep(0.1)

#Start the screen
def run_screen():
    screen_conn, dh_conn = Pipe(False) #Open a pipe for the screen

    #Create the screen daemon and pass it the pipe
    screenDaemon = Process(target=start_screen, args=(screen_conn,), daemon=True) 
    screenDaemon.start() #start the screen daemon

    #Create the updater daemon and pass it the our end of the pipe
    updaterDaemon =  Thread(target=update_screen, args=(dh_conn,), daemon=True)
    updaterDaemon.start() #start the updater daemon


    
if __name__ == "__main__":
    run()
