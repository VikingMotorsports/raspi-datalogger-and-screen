import board
import time
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

connected = 0;
try:
    i2c = board.I2C()
    accelor = LSM6DSOX(i2c)
    connected = 1;
except:
    connected = 0;

def getData():
    global connected, accelor
    if connected == 0:
        try:
            i2c = board.I2C()
            accelor = LSM6DSOX(i2c)
            connected = 1
        except:
            connected = 0
    elif connected == 1:
        x,y,z = accelor.acceleration
        a,b,c = accelor.gyro
        return x,y,z,a,b,c
    return ["ERR", "ERR", "ERR", "ERR", "ERR", "ERR"]

def printData():
    global connected, accelor
    if 1 == connected:
        print("\nAccel:")
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelor.acceleration))
        print("Gyro: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelor.gyro))
    else:
        try:
            i2c = board.I2C()
            accelor = LSM6DSOX(i2c)
            connected = 1
        except:
            connected = 0
        print("ERROR")

if __name__ == "__main__":
    try:
        while 1:
            printData()
            time.sleep(0.1)
    except KeyboardInterrupt: #ctrl-c
        exit()
