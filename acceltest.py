import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

i2c = board.I2C()
accelor = LSM6DSOX(i2c)

def getAccel():
	x,y,z = accelor.acceleration
	return int(x + y+ z)


