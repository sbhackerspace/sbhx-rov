#!/usr/bin/env python
#
# Major mods by Roger Burnham January 2012
# from the rov_joystick module started by Steve Phillips
#

import argparse
import logging
import platform
import pygame
import serial
import sys
import time
from ArduinoPorts import findServoPort
from math import floor

sysPlatform = platform.system()
usbPort, dev = None, None

X_AXIS = 0
Y_AXIS = 1
THROTTLE_AXIS = 2 # Throttle
Z_AXIS = 3
RUDDER_AXIS = 4

BUTTONS = {0: 'Trigger',
			1: 'Action 2',
			2: 'Action 3',
			3: 'Action 4',
			4: 'Action 5',
			5: 'Action 6',
			6: 'Action 7',
			7: 'Action 8',
			8: 'Action 9',
			9: 'Action 10',
			10: 'ST',
			11: 'SE'}
			
# lambda to convert integer into a string of the binary representation
bstr = lambda n, l=16: n<0 and binarystr((2L<<l)+n) or n and bstr(n>>1).lstrip('0')+str(n&1) or '0'

# allow multiple joysticks
joy = []

def logJoyDict(e):
	for k in e.dict.keys():
		logging.debug('   %s->%s' % (k, `e.dict[k]`))

def fix(bits):
	if bits & 0b00100000:
		return 63-bits
	else:
		return bits

# handle joystick event
def handleJoyEvent(e):
	if e.type == pygame.JOYAXISMOTION:
		axis = "unknown"
		bits = 0b00000000 
		if (e.dict['axis'] == X_AXIS):
			axis = "X"
			bits = 0b10000000 # Throw away; don't change anything

		if (e.dict['axis'] == Y_AXIS):
			axis = "Y"
			bits = 0b10000000

		if (e.dict['axis'] == THROTTLE_AXIS):
			axis = "T"
			bits = 0b01000000

		if (e.dict['axis'] == Z_AXIS):
			axis = "Z"
			bits = 0b11000000

		if (axis != "unknown"):
			logging.debug('JoyAxisEvent %s %s %s, bitmask: %s' % (e.type, axis, pygame.event.event_name(e.type), bstr(bits)))
			
			scale  = 63  # From 0 to __
			scale /= 2
			bottom5 = int( scale*(e.dict['value']+1) )
			logging.debug("   From joystick: %s %s" % (axis, bottom5))
			logging.debug("      bits+bottom5: %s" % `bits+bottom5`)

			dev.write(chr(bits+bottom5))
			logging.debug("   %s %f" % (axis, e.dict['value']+1))
			from_arduino = dev.read(1)
			logging.debug("   from_arduino: %s" % `from_arduino`)
			time.sleep(.030)
			# for num in range(256):
			#     print "Sending " + str(num)
			#     dev.write(chr(num))
			#     time.sleep(.005)

			# Arduino joystick-servo hack
			if (axis == "X"):
				pos = e.dict['value']
				# convert joystick position to servo increment, 0-180
				move = round(pos * 90, 0)
				if (move < 0):
					serv = int(90 - abs(move))
				else:
					serv = int(move + 90)
				# convert position to ASCII character
				servoPosition = serv
				# and send to Arduino over serial connection
				logging.debug("???servo.move(1, %s)" % servoPosition)

			# Arduino joystick-servo hack
			if (axis == "Y"):
				pos = e.dict['value']
				# convert joystick position to servo increment, 0-180
				move = round(pos * 90, 0)
				if (move < 0):
					serv = int(90 - abs(move))
				else:
					serv = int(move + 90)
				# convert position to ASCII character
				servoPosition = serv
				# and send to Arduino over serial connection
				logging.debug("???servo.move(2, %s)" % servoPosition)

		elif e.dict['axis'] == RUDDER_AXIS:
			rudderVal = e.dict['value']
			logging.debug('RudderEvent %s %s -> %.4f' % (e.type, pygame.event.event_name(e.type), rudderVal))
			
		else:
			logging.error('unknown axis: %s' % `e.dict['axis']`)
			logJoyDict(e)
			
	elif e.type == pygame.JOYHATMOTION:
		xVal, yVal = e.dict['value']
		logging.debug('JoyHatEvent %s %s -> %s' % (e.type, pygame.event.event_name(e.type), `(xVal, yVal)`))
	
	elif e.type == pygame.JOYBUTTONDOWN:
		button = e.dict['button']
		logging.debug('JoyButtonDownEvent %s  %s -> %s' % (e.type, pygame.event.event_name(e.type), BUTTONS[button]))
	
	elif e.type == pygame.JOYBUTTONUP:
		button = e.dict['button']
		logging.debug('JoyButtonUpEvent %s  %s -> %s' % (e.type, pygame.event.event_name(e.type), BUTTONS[button]))
		

# wait for joystick input
def joystickControl():
	logging.info('entering joystick control loop')
	while 1:
		e = pygame.event.wait()
		if (e.type in [pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION]):
			handleJoyEvent(e)
		else:
			logging.debug('unhandled event %s: %s' % (`e.type`, pygame.event.event_name(e.type)))
			logJoyDict(e)
 
# main method
def main():
	global dev, usbport
	
	logLevel = logging.INFO

	parser = argparse.ArgumentParser(description='Joystick control of a servo')
	parser.add_argument('-debug', action='store_true')
	args = parser.parse_args()
	if args.debug:
		logLevel = logging.DEBUG
		
	# set up logging to file - see previous section for more details
	logging.basicConfig(level=logLevel,
						format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						datefmt='%m-%d %H:%M',
						filename='./%s.log' % sys.argv[0],
						filemode='w')
	# define a Handler which writes INFO messages or higher to the sys.stderr
	console = logging.StreamHandler()
	console.setLevel(logging.DEBUG)
	# set a format which is simpler for console use
	formatter = logging.Formatter('%(name)-6s: %(levelname)-8s %(message)s')
	# tell the handler to use this format
	console.setFormatter(formatter)
	# add the handler to the root logger
	logging.getLogger('').addHandler(console)

	usbPort, dev = findServoPort()
	logging.info('Arduino servo found on part %s' % usbPort)

	# initialize pygame
	logging.info('initializing joystick...')
	pygame.joystick.init()
	logging.info('initializing display...')
	pygame.display.init()
	if not pygame.joystick.get_count():
		logging.error('Please connect a joystick and run again.')
		quit()
	for i in range(pygame.joystick.get_count()):
		myjoy = pygame.joystick.Joystick(i)
		myjoy.init()
		joy.append(myjoy)
		logging.debug("Joystick %d: " % (i+1) + joy[i].get_name())

	# run joystick listener loop
	joystickControl()
 
# allow use as a module or standalone script
if __name__ == "__main__":
	main()
