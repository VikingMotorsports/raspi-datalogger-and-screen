import time
import serial


def tradeData(data, ser):
    try:
        recieved_data = ser.read() #read serial port
        sleep(0.03)
        data_left = ser.inWaiting() #check for remianing byte
        received_data += ser.read(data_left)

        if received_data:
            ser.write(data)
        else: 
            received_data = bytes(["ERR"])

        return received_data
    except:
        return bytes(["ERR"])


def loop(connection):
    try:
        ser = serial.Serial("/dev/ttyS0", 115200) #Open port with baud rate
        ser.reset_input_buffer()
        while 1:
            toSend = connection.recv() 
            
            connection.send(tradeData(toSend, ser))
            print(str(data) + "\n")
    except:
        return

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        exit()

