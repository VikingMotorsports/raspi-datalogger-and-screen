import time

def wait():
    for i in range(1,6):
        time.sleep(1)
        print(i)

if __name__ == "__main__":
    wait()
