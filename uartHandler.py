import time
import serial
import numpy as np


terminator = bytes([255])
def tradeData(ser):
    try:
        received_data = ser.read_until(terminator) #read serial port

        if not received_data:
            received_data = bytes([0])

        return received_data
    except:
        return bytes([0])


def loop(connection):
    while 1:
        try:
            ser = serial.Serial("/dev/ttyS0", 115200) #Open port with baud rate
            ser.reset_input_buffer()
            while 1:
                data = np.frombuffer(tradeData(ser), dtype=np.ubyte)
                connection.send(data)
                #print(str(len(data)))
        except:
            print("ERROR WITH UART");

def test():
    while 1:
        try:
            ser = serial.Serial("/dev/ttyS0", 115200) #Open port with baud rate
            ser.reset_input_buffer()
            while 1:
                data = tradeData(ser)                
                print(str(data) + "\n")
        except:
            print("ERROR WITH UART");


if __name__ == "__main__":
    try:
        test()
    except KeyboardInterrupt:
        exit()

