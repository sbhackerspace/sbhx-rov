#!/usr/bin/env python
#
# Written by Roger Burnham, January 2012
#

import platform
import serial
import logging

sysPlatform = platform.system()
def findServoPort():
# http://pyserial.sourceforge.net/pyserial_api.html#module-serial.tools.list_ports 
# serial.tools.list_ports does not work for me on win7.
# 
# C:\>python -m serial.tools.list_ports
# no ports found
# 
# so, I'll roll my own
#
	tstPort = 'COM'
	if sysPlatform == 'Windows':
		usbPort = 'COM'
	elif sysPlatform == 'Linux':
		usbPort = '/dev/ttyUSB'
#	elif sysPlatform == 'Darwin':
#		No idea what to do here (Roger)...
#		usbPort = '/dev/tty.usbserial-FTALLOK2'
		raise IOError, 'Do not know how to find all serial ports on a Macintosh'
	else:
		raise IOError, 'Unknown platform %s, cannot find all serial ports' % sysPlatform
	n = 0
	while 1:
		usbPort = '%s%d' % (tstPort, n)
		try:
			logging.debug('testing port %s' % usbPort)
			dev = serial.Serial(usbPort, baudrate=9600, timeout=1)
			break
		except: serial.SerialException
		n += 1
		if n > 9: raise serial.SerialException, 'Servo USB serial port not found in first 10 ports'
		# got the port, is it a servo?
		
	return usbPort, dev

if __name__ == "__main__":
	port, device = findServoPort()
	print 'found device on port %s, trying to read a line...' % port
	device.close()
