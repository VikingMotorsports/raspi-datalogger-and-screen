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
    if 1 == connected:
        x,y,z = accelor.acceleration
        a,b,c = accelor.gyro
        return x,y,z,a,b,c
    return 1,2,3,4,5,6

def printData():
    print("\nAccel:")
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelor.acceleration))
    print("Gyro: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelor.gyro))

if __name__ == "__main__":
    try:
        while 1:
            printData()
            time.sleep(0.1)
    except KeyboardInterrupt: #ctrl-c
        exit()
