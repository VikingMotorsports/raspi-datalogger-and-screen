import time
import pigpio

I2C_ADDR=0x69

def i2c(id, tick):
    global pi

    status, count, data = pi.bsc_i2c(I2C_ADDR)

    if count:
        print("recieved: {}".format(data))
            
        status, count, data = pi.bsc_i2c(I2C_ADDR, data)

pi = pigpio.pi()

if not pi.connected:
    exit()

#Respond to BSC slave activity

e = pi.event_callback(pigpio.EVENT_BSC, i2c)

pi.bsc_i2c(I2C_ADDR) #configure BSC as I2C slave

time.sleep(600)

e.cancel()

pi.bsc_i2c(0)

pi.stop()


