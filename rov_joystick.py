#!/usr/bin/env python
import pygame
from math import floor
from pylibftdi import Device # I2C over USB
import time
#import servo
dev = Device(mode='b')
dev.baudrate = 9600

# allow multiple joysticks
joy = []

def fix(bits):
    if bits & 0b00100000:
        return 63-bits
    else:
        return bits

# handle joystick event
def handleJoyEvent(e):
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 0):
            axis = "X"
            bits = 0b10000000 # Throw away; don't change anything
 
        if (e.dict['axis'] == 1):
            axis = "Y"
            bits = 0b10000000
 
        if (e.dict['axis'] == 2):
            axis = "Throttle"
            bits = 0b01000000
 
        if (e.dict['axis'] == 3):
            axis = "Z"
            bits = 0b11000000
 
        if (axis != "unknown"):
            scale  = 63  # From 0 to __
            scale /= 2
            bottom5 = int( scale*(e.dict['value']+1) )
            print "From joystick: %s %d" % (axis, bottom5)
            print "bottom5 ==", bottom5
            print "bits+bottom5 == ", bits+bottom5
            print 

            dev.write(chr(bits+bottom5))
            print "%s %f" % (axis, e.dict['value']+1)
            from_arduino = dev.read(1)
            print "from_arduino:", from_arduino
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
                ##print "servo.move(1, %s)" % servoPosition
 
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
                ##print "servo.move(2, %s)" % servoPosition
 
    # elif e.type == pygame.JOYBUTTONDOWN:
    #     str = "Button: %d" % (e.dict['button'])
    #     # uncomment to debug
    #     output(str, e.dict['joy'])
    #     # Button 0 (trigger) to quit
    #     if (e.dict['button'] == 0):
    #         print "Pew Pew You're DEAD!!\n"
    #     if (e.dict['button'] == 8):
    #         print "Bye!\n"
    #         quit()
    # else:
    #     pass

# wait for joystick input
def joystickControl():
    while True:
        e = pygame.event.wait()
        if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN):
            handleJoyEvent(e)
 
# main method
def main():
    # initialize pygame
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print "\nPlease connect a joystick and run again.\n"
        quit()
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        #print "Joystick %d: " % (i) + joy[i].get_name()
 
    # run joystick listener loop
    joystickControl()
 
# allow use as a module or standalone script
if __name__ == "__main__":
    main()
