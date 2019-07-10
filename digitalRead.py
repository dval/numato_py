#This demo code demonstrates how to read the status of a GPIO


import sys
import serial

if (len(sys.argv) < 3):
	print "Usage: gpioread.py <PORT> <GPIONUM>\nEg: gpioread.py COM1 0"
	sys.exit(0)
else:
	portName = sys.argv[1];
	gpioNum = sys.argv[2];

#Open port for communication	
serPort = serial.Serial(portName, 19200, timeout=1)

#Send "gpio read" command. GPIO number 10 and beyond are
#referenced in the command by using alphabets starting A. For example
#GPIO10 willbe A, GPIO11 will be B and so on. Please note that this is
#not intended to be hexadecimal notation so the the alphabets can go 
#beyond F.

if (int(gpioNum) < 10):
    gpioIndex = str(gpioNum)
else:
    gpioIndex = chr(55 + int(gpioNum))

serPort.write("gpio read "+ gpioIndex + "\r")

response = serPort.read(25)

if(response[-4] == "1"):
	print "GPIO " + str(gpioNum) +" is ON"
	
elif(response[-4] == "0"):
	print "GPIO " + str(gpioNum) +" is OFF"
	
#Close the port
serPort.close()
