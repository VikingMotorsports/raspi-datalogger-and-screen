#!/usr/bin/env python3
import boot
import dataHandler

#<',=,~~
#   rat to eat bugs

if __name__ == "__main__":
    boot = Process(target=boot.wait)
    dataHandler = Process(target=dataHandler.run)

    boot.start() #Run boot process and wait for it to finish
    boot.join()

    dataHandler.start() #Run data handler process and wait for it to finish
    dataHandler.join()
