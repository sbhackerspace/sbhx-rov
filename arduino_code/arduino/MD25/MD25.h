/*
  Morse.h - Library for flashing Morse code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/

#ifndef MD25_h
#define MD25_h

#include "WProgram.h"
#include "Wire.h"

#define softwareReg 0x0D                                    // Byte to read the software version
#define speed1 0x00                                         // Byte to send speed to first motor
#define speed2 0x01                                         // Byte to send speed to second motor
#define cmdByte 0x10                                        // Command byte
#define mvCsr 0x02                                          // Command for LCD03 to move cursor
#define hideCsr 0x04                                        // Byte to hide LCD03 cursor
#define clrScrn 0x0C                                        // Byte to clear LCD03 screen
#define encoderOne 0x02                                     // Byte to read motor encoder 1
#define encoderTwo 0x06                                     // Byte to read motor encoder 2
#define voltRead 0x0A                                       // Byte to read battery volts

class MD25
{
  public:
    MD25(byte address);
	void changeAddress(byte newAddress);
	void stopMotor();
	void changeSpeed(byte controller, byte motor, byte speed);
	void test();
  private:
	byte _address;
};

#endif

