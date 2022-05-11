import board
import time
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

i2c = board.I2C()
accelor = LSM6DSOX(i2c)

def getAccel():
	x,y,z = accelor.acceleration
	return int(x + y+ z)

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
