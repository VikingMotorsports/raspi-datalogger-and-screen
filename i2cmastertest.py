from smbus2 import SMBus, i2c_msg
import time

with SMBus(1) as bus:
    while 1:
    # Write a single byte to address 0x69
        toSend = input("Enter Message: ")
        msg = i2c_msg.write(0x69, toSend)
        bus.i2c_rdwr(msg)
 
        msg = i2c_msg.read(0x69, 18 + len(toSend))
        bus.i2c_rdwr(msg)
        data = list(msg)
        res = ""
        for i in data:
            res += chr(i)
        res += '\n'

        print(res)
