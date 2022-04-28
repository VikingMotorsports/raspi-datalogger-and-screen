import tim
from multiprocessing import Process, Pipe
from screen import start_screen

#<',=,~~
#   rat to eat bugs

def run():
    run_screen()
    
    mph = 0
    bat = 30
    coolTemp = 0
    batTemp = 3
    motTemp = 6

#Pass the screen updated info
def update_screen(connection):
    while 1:

        for i in range(0,70):
            mph += 1
            bat += 1
            coolTemp += 1
            batTemp += 1
            motTemp += 1

            time.sleep(0.1)

        for i in range(0,70):
            mph -= 1
            bat -= 1
            coolTemp -= 1
            batTemp -= 1
            motTemp -= 1

            time.sleep(0.1)

#Start the screen
def run_screen():
    screen_conn, dh_conn = Pipe(False) #Open a pipe for the screen
    screen = Process(target=start_screen, arguments=screen_conn, daemon=True) #Create the screen daemon and pass it the pipe
    screen.start() #start the screen daemon

    
if __name__ == "__main__":
    test()
