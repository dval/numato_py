
# This demo code demonstrates how to write PWM to GPIOs

import time, sys, signal, serial

# hardware
allPins = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V"]
working = ["8","G","O"] # 8, 16, 24
reg_a = 0x000000ff
reg_b = 0x0000ff00
reg_c = 0x00ff0000
reg_d = 0xff000000

currentMask = 0x00000000

# handler for exiting the loop gracefully
def interupt_handler(signal, frame):
	print("\nprogram exiting ...")
	doHousekeeping()
	sys.exit(0)


# clean up
def doHousekeeping():
	# clear pins
	pdat = "gpio iomask ffffffff\r"
	serPort.write(bytes(pdat, 'UTF-8'))
	time.sleep(0.05) 		# pause after updating iomask
	for p in allPins:
		pdat = "gpio clear " + p + "\r"
		serPort.write(bytes(pdat, 'UTF-8'))
		time.sleep(0.005) 	# ~200 Hz. shortest timing to send repeated msgs

	# Close the port
	serPort.close()
	print ("clean up done.")

# this returns the Numato iomask string from a hexidecimal number
def registerMask(hexString):
	return format(hexString, '#010x')[2:]


# script global variables 
command = "set"
gpioIndex = 0
portName, serPort = '',''

# pwm stuff
pwm_resolution = 1024
pwm_pulse = 0
pwm_timers = [ [0,220], [1,512], [2,1000] ]

def setup():
	global portName, serPort
	# assign keyboard interupt listener
	signal.signal(signal.SIGINT, interupt_handler)
	
	# this is what the USB GPIO shows up as:
	portName = "/dev/tty.usbmodem1421"
	#portName = "com6"

	# open port for communication	
	serPort = serial.Serial(portName, 19200, timeout=1)

	pdat = "gpio clearall\r"
	serPort.write(bytes(pdat, 'UTF-8'))
	time.sleep(0.01)

	pdat = "gpio iodir 00000000\r"
	serPort.write(bytes(pdat, 'UTF-8'))
	time.sleep(0.01)


def testRegisters():
	global currentMask

	#currentMask = reg_b | reg_c | reg_d
	
	pdat = "gpio iomask " + registerMask(currentMask) + "\r"
	serPort.write(bytes(pdat, 'UTF-8'))
	time.sleep(0.05)

	currentMask = currentMask | 0x1010100

	pdat = "gpio iomask " + registerMask(currentMask) + "\r"
	serPort.write(bytes(pdat, 'UTF-8'))
	time.sleep(0.05)

	pdat = "gpio writeall ffffffff\r"
	serPort.write(bytes(pdat, 'UTF-8'))
	time.sleep(0.01)


def run():
	while True:


		time.sleep(0.02) # ~50 Hz servo
		#time.sleep(0.001) # ~1kHz 


# start interuptable loop
# while True:

# 	# gpioIndex = gpioIndex+1
# 	# if gpioIndex > 2:
# 	# 	gpioIndex = 0
# 	# command = "set" if command is "clear" else "clear"
# 	# pdat = "gpio " + command + " " + working[gpioIndex] + "\r"
# 	# serPort.write(bytes(pdat, 'UTF-8'))

# 	# trigger PWM pulse
# 	if pwm_pulse > pwm_resolution:
# 		pwm_pulse = 0
# 	pwm_pulse = pwm_pulse + 1
# 	# check pwm array to see if pin is still on
# 	pwcmd = " "
# 	#for pwt in pwm_timers:
# 		pwcmd = "gpio set " + str(working[pwt[0]]) + "\r"
# 		if pwt[1] < pwm_pulse:
# 			pwcmd = "gpio clear " + str(working[pwt[0]]) + "\r"
# 		time.sleep(0.001)  # 1024 Hz

# 		serPort.write(bytes(pwcmd, 'UTF-8'))
# 	# print (pwm_pulse)

# 	# this sets PWM frequency
# 	#time.sleep(0.001)  # 1024 Hz

	
if __name__ == "__main__":
	setup()
	#
	while True:
		testRegisters()
		#pass