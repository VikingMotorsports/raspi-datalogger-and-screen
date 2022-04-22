#!/user/bin/env python3
import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#create Rpi = busio.SPI(clock-board.SCK, MISO=b

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D25)
mcp = MCP.MCP3008(spi, cs)
# pot12 = AnalogIn(mcp, MCP.P0)
# pot13 = AnalogIn(mcp, MCP.P0)
# pot14 = AnalogIn(mcp, MCP.P0)
# pot15 = AnalogIn(mcp, MCP.P0)
# pot16 = AnalogIn(mcp, MCP.P0)
# pot17 = AnalogIn(mcp, MCP.P0)
# pot18 = AnalogIn(mcp, MCP.P0)
# 
# pot23 = AnalogIn(mcp, MCP.P0)
# pot22 = AnalogIn(mcp, MCP.P0)
# pot23 = AnalogIn(mcp, MCP.P0)
# pot24 = AnalogIn(mcp, MCP.P0)
# pot25 = AnalogIn(mcp, MCP.P0)
# pot26 = AnalogIn(mcp, MCP.P0)
# pot27 = AnalogIn(mcp, MCP.P0)
# pot28 = AnalogIn(mcp, MCP.P0)
# 
# pot31 = AnalogIn(mcp, MCP.P0)
# pot32 = AnalogIn(mcp, MCP.P0)
# pot32 = AnalogIn(mcp, MCP.P0)
# pot33 = AnalogIn(mcp, MCP.P0)
# pot34 = AnalogIn(mcp, MCP.P0)
# pot35 = AnalogIn(mcp, MCP.P0)
# pot36 = AnalogIn(mcp, MCP.P0)
# pot37 = AnalogIn(mcp, MCP.P0)
# pot38 = AnalogIn(mcp, MCP.P0)
# 
# pot41 = AnalogIn(mcp, MCP.P0)
# pot42 = AnalogIn(mcp, MCP.P0)
# pot44 = AnalogIn(mcp, MCP.P0)
# pot44 = AnalogIn(mcp, MCP.P0)
# pot45 = AnalogIn(mcp, MCP.P0)
# pot46 = AnalogIn(mcp, MCP.P0)
# pot47 = AnalogIn(mcp, MCP.P0)
# pot48 = AnalogIn(mcp, MCP.P0)

while True:
    pot11 = AnalogIn(mcp, MCP.P0)
    print("Raw ADC Value: ", pot11.value)
    print("ADC Voltage: " + str(pot11.voltage) + "V")
    time.sleep(0.5)
