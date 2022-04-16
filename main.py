import multiprocessing
import boot
import dataHandler

if __name__ == "__main__":
    boot = multiprocessing.Process(target=boot.wait)
    dataHandler = multiprocessing.Process(target=dataHandler.run)

    boot.start()
    boot.join()
    dataHandler.start()
    dataHandler.join()
