import multiprocessing
import Boot
import DataHandler

if __name__ == "__main__":
    boot = multiprocessing.Process(target=Boot.wait, args=())
    dataHandler = multiprocessing.Process(target=DataHandler.test, args=())

    boot.start()
    boot.join()
    dataHandler.start()
    dataHandler.join()
