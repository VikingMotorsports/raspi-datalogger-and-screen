import board
import adafruit_mcp9808
import time

i2c = board.I2C()
mcp = adafruit_mcp9808.MCP9808(i2c)

def getTemp():
	return int(mcp.temperature)
