from smbus2 import SMBus, i2c_msg
from random import randint

slaveAddress = 0x69

def tradeData(data1, data2):
    try:
        with SMBus(1) as bus:
            toSend = [data1, data2]
            send = i2c_msg.write(slaveAddress, toSend)
            rec = i2c_msg.read(slaveAddress, 4)
            bus.i2c_rdwr(send, rec)
            return list(rec)
    except:
        return ["ERROR", "ERROR", "ERROR", "ERROR"]

def loop():
        while 1:
            data1 = randint(0,3)
            data2 = randint(0,3)
            
            data = tradeData(data1, data2)
            print(str(data) + "\n")




if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        exit()

