#This demo code demonstrates how to read analog channel


import sys
import serial

if (len(sys.argv) < 3):
	print "Usage: analogread.py <PORT> <Analog Channel>\nEg: analogread.py COM1 0"
	sys.exit(0)
else:
	print sys.argv
	portName = sys.argv[1];
	analogChannel = sys.argv[2];

#Open port for communication	
serPort = serial.Serial(portName, 19200, timeout=1)

#Send "adc read" command
serPort.write("adc read "+ str(analogChannel) + "\r")

response = serPort.read(25)
print response ##[10:-3]
	
#Close the port
serPort.close()
