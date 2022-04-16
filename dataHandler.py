import time
import threading
import screen

def run():
    run_screen()
    
    mph = 0;
    bat = 30;
    coolTemp = 0;
    batTemp = 3;
    motTemp = 5;
    valDict = {
            "mph": mph,
            "bat": bat,
            "coolTemp": coolTemp,
            "motTemp": motTemp,
            "batTemp": batTemp
            }

    while 1:

        for i in range(0,70):
            mph += 1;
            bat += 1;
            coolTemp += 1;
            batTemp += 1;
            motTemp += 1;

            screen.update(mph, bat, coolTemp, batTemp, motTemp)
            time.sleep(0.1)

        for i in range(0,70):
            mph -= 1;
            bat -= 1;
            coolTemp -= 1;
            batTemp -= 1;
            motTemp -= 1;

            screen.update(mph, bat, coolTemp, batTemp, motTemp)
            time.sleep(0.1)

def run_screen():
    screenDaemon = threading.Thread(target=screen.start_screen, daemon=True)
    screenDaemon.start()
    
if __name__ == "__main__":
    test()
