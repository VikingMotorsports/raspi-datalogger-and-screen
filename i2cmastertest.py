from smbus2 import SMBus, i2c_msg
from random import randint

slaveAddress = 0x69
with SMBus(1) as bus:
    while 1:
        toSend = bytes([randint(1, 12), randint(1,12)])
        
        send = i2c_msg.write(slaveAddress, toSend)
        rec = i2c_msg.read(slaveAddress, 3)
        bus.i2c_rdwr(send, rec)
        data = list(rec)
        print("Sent: " + str(toSend))
        print(str(data))
