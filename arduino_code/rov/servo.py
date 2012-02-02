#!/usr/bin/env python

################################################
# Module:   servo.py
# Created:  2 April 2008
# Author:   Brian D. Wendt
#   http://principialabs.com/
# Version:  0.2
# License:  GPLv3
#   http://www.fsf.org/licensing/
'''
Provides a serial connection abstraction layer
for use with Arduino "MultipleServos" sketch.
'''
################################################

import serial

usbport = '/dev/ttyUSB0'
ser = serial.Serial(usbport, 9600, timeout=1)
#print ser

def move(servo, angle):
    '''Moves the specified servo to the supplied angle.

    Arguments:
        servo
          the servo number to command, an integer from 1-4
        angle
          the desired servo angle, an integer from 0 to 180

    (e.g.) >>> servo.move(2, 90)
           ... # "move servo #2 to 90 degrees"'''

    if (0 <= angle <= 180):
        ser.write(chr(255))
        ser.write(chr(servo))
        ser.write(chr(angle))
    else:
        print "Servo angle must be an integer between 0 and 180.\n"