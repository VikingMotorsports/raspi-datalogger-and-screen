import time
import pisotest
import adctest
import acceltest

#<',=,~~
#   rat to eat bugs

def main():
    pisotest.setup()

    while 1:
        print("="*40)
        pisotest.printData()
        adctest.printData()
        acceltest.printData()
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: #ctrl-c
        pisotest.cleanup()
        
