import mcp3008
import time

#initialize mcp3008
adc = mcp3008.MCP()


def read(): #print out the values of each potentionmeter
    print(adc.read([mcp3008.CH0]), adc.read([mcp3008.CH1]), adc.read[mcp3008.CH2], adc.read([mcp3008.CH3]), adc.read([mcp3008.CH4]), adc.read([mcp3008.CH5]), adc.read([mcp3008.CH6]), adc.read([mcp3008.CH7]))

def loop(): #read 10 times a second
    while True:
        read()
        time.sleep(0.1)

try:
    loop()
except KeyboardInterrupt: #ctrl-c
    GPIO.cleanup()

