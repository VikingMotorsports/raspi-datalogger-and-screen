from smbus2 import SMBus, i2c_msg

slaveAddress = 0x69
with SMBus(1) as bus:
    while 1:
       # toSend = input("Enter Message: ")
       # send = i2c_msg.write(slaveAddress, toSend)
        rec = i2c_msg.read(slaveAddress, 18)# + len(toSend))
        bus.i2c_rdwr(rec)
        data = list(rec)
        res = ""
        for i in data:
            res += chr(i)
        res += "\n"

        print(res)
