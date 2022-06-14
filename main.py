#!/usr/bin/env python3
from multiprocessing import Process
import dataHandler
import ready
import sys

#<',=,~~
#   rat to eat bugs

if __name__ == "__main__":
    try:
        readyHandler = Process(target=ready.run, daemon=True)
        dataHandler = Process(target=dataHandler.run)

        readyHandler.start()
        dataHandler.start() #Run data handler process and wait for it to finish
        dataHandler.join()
    except KeyboardInterrupt:
        sys.exit()
