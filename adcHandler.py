#!/user/bin/env python3
import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#create Rpi = busio.SPI(clock-board.SCK, MISO=b
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs1 = digitalio.DigitalInOut(board.D16)
mcp1 = MCP.MCP3008(spi, cs1)

cs2 = digitalio.DigitalInOut(board.D20)
mcp2 = MCP.MCP3008(spi, cs2)

pot11 = AnalogIn(mcp1, MCP.P0)
pot12 = AnalogIn(mcp1, MCP.P1)
pot13 = AnalogIn(mcp1, MCP.P2)
pot14 = AnalogIn(mcp1, MCP.P3)
pot15 = AnalogIn(mcp1, MCP.P4)
pot16 = AnalogIn(mcp1, MCP.P5)
pot17 = AnalogIn(mcp1, MCP.P6)
pot18 = AnalogIn(mcp1, MCP.P7)

pot21 = AnalogIn(mcp2, MCP.P0)
pot22 = AnalogIn(mcp2, MCP.P1)
pot23 = AnalogIn(mcp2, MCP.P2)
pot24 = AnalogIn(mcp2, MCP.P3)
pot25 = AnalogIn(mcp2, MCP.P4)
pot26 = AnalogIn(mcp2, MCP.P5)
pot27 = AnalogIn(mcp2, MCP.P6)
pot28 = AnalogIn(mcp2, MCP.P7)

def printData():
    print("\nADCs")
    print(str(pot11.voltage) + "\t" + str(pot12.voltage) + "\t" + str(pot13.voltage) + "\t" + str(pot14.voltage) + "\t" + str(pot15.voltage) + "\t" + str(pot16.voltage) + "\t" + str(pot17.voltage) + "\t" + str(pot18.voltage))
    print(str(pot21.voltage) + "\t" + str(pot22.voltage) + "\t" + str(pot23.voltage) + "\t" + str(pot24.voltage) + "\t" + str(pot25.voltage) + "\t" + str(pot26.voltage) + "\t" + str(pot27.voltage) + "\t" + str(pot28.voltage))
    print()

def getData():
    return [pot11.value, pot12.value, pot13.value, pot14.value, 
            pot16.value, pot16.value, pot17.value, pot18.value,
            pot21.value, pot22.value, pot23.value, pot24.value, 
            pot25.value, pot26.value, pot27.value, pot28.value]

if __name__ == "__main__":
    try:
        while True:
            printData()
            time.sleep(0.5)
    except KeyboardInterrupt: #ctrl-c
        exit()
