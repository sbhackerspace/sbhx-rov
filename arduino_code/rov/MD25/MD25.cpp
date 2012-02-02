/*
  MD25.cpp - Library for controlling .
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/

#include "WProgram.h"
#include "MD25.h"
#include "Wire.h"

MD25::MD25(byte address)
{
  Wire.begin();
  _address = address;
}


/**
** Change MD25 Address
** This can be really tricky as the input requres the address to be right-shifted 1
** and the output requires the address to be normal.
**
** @param {byte} currentAddress Current MD25 address Rightshifted 1
** @param {byte} newAddress Desired MD25 address Non-Rightshifted 1
**
** @returns {int} 1 for error, 0 for all good
**/
void MD25::changeAddress(byte currentAddress, byte newAddress){  
       
	   Wire.beginTransmission(currentAddress);
       Wire.send(cmdByte);
       Wire.send(0xA0);
       Wire.endTransmission();
       delay(5); 
       
       Wire.beginTransmission(currentAddress); 
       Wire.send(cmdByte);
       Wire.send(0xAA);  
       Wire.endTransmission();
       delay(5);  
       
       Wire.beginTransmission(currentAddress); 
       Wire.send(cmdByte);
       Wire.send(0xA5);
       Wire.endTransmission(); 
       delay(5); 
       
       Wire.beginTransmission(currentAddress); 
       Wire.send(cmdByte);
       Wire.send(newAddress);
       Wire.endTransmission(); 
       delay(100);        
}

void MD25::stopMotor(){                                           // Function to stop motors
	  Wire.beginTransmission(0x58);
	  Wire.send(speed2);
	  Wire.send(128);                                         
	  Wire.endTransmission();
	  
	  Wire.beginTransmission(0x58);
	  Wire.send(speed1);
	  Wire.send(128);                               
	  Wire.endTransmission();
} 

void MD25::changeSpeed(){                                           // Function to stop motors
	   Wire.beginTransmission(88);
       Wire.send(speed2);
       Wire.send(1);
       Wire.endTransmission();
       delay(5);
	  
	  Wire.beginTransmission(88);
	  Wire.send(speed1);
	  Wire.send(1);                               
	  Wire.endTransmission();
} 

void MD25::test(){                                           // Function to stop motors
	Serial.begin(9600);
	Serial.println(_address, HEX);
} 