#!/usr/bin/env python3
from multiprocessing import Process
import boot
import dataHandler
import sys

#<',=,~~
#   rat to eat bugs

if __name__ == "__main__":
    try:
        boot = Process(target=boot.wait)
        dataHandler = Process(target=dataHandler.run)

        boot.start() #Run boot process and wait for it to finish
        boot.join()

        dataHandler.start() #Run data handler process and wait for it to finish
        dataHandler.join()
    except KeyboardInterrupt:
        sys.exit()
