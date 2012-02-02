//Interface Arduino USB with Parallax 28440 125 Khz UART RFID Reader/Writer
//Program reads a EM4x50 tag and reports the ID on the serial monitor.
//Coded by Uberdude

#include "NewSoftSerial.h"
#define txPin 13
#define rxPin 12

//Reader/Writer Commands
#define RFID_READ 0x01
#define RFID_WRITE 0x02
#define RFID_LOGIN 0x03
#define RFID_PROTECT 0x05
//#define RFID_LEGACY 0x0F

NewSoftSerial mySerial(rxPin, txPin);
int val = 0; 
//char code[6]; //Note this is 11 for the extra null char?
//int bytesread = 0;
//int flag = 0;

//Tags
//char TAG1[11] = "0800E28C60";
//char TAG2[11] = "0800D9E43E";

void setup()
{
Serial.begin(9600);
mySerial.begin(9600);

// pinMode(2, OUTPUT);
// pinMode(4, OUTPUT);
pinMode(txPin, OUTPUT); //pin 13
pinMode(rxPin, INPUT); //pin 12

Serial.println("RFID Write Normal");
}

void loop()
{ 
mySerial.print("!RW");
mySerial.print(RFID_WRITE, BYTE);
mySerial.print(3, BYTE);
mySerial.print(0xCC, BYTE);
mySerial.print(0xCC, BYTE);
mySerial.print(0xCC, BYTE);
mySerial.print(0xCC, BYTE);

//Error code read
if(mySerial.available() > 0) { // if data available from reader 
val = mySerial.read();
if(val != 255){
Serial.print("Write Error Code:");
Serial.println(val, HEX);
}
} 

mySerial.print("!RW");
mySerial.print(RFID_READ, BYTE);
mySerial.print(3, BYTE);

//0th read
if(mySerial.available() > 0) { // if data available from reader 
val = mySerial.read();
if(val != 255){
Serial.print("Read Error Code:");
Serial.println(val, HEX);
}
} 

//1st byte
if(mySerial.available() > 0) { // if data available from reader 
val = mySerial.read();
if(val != 255){
Serial.print("1st:");
Serial.println(val, HEX);
}
} 

//2nd byte
if(mySerial.available() > 0) { // if data available from reader 
val = mySerial.read();
if(val != 255){
Serial.print("2nd:");
Serial.println(val, HEX);
}
} 

//3rd byte
if(mySerial.available() > 0) { // if data available from reader 
val = mySerial.read();
if(val != 255){
Serial.print("3rd:");
Serial.println(val, HEX);
}
} 

//4th byte

if(mySerial.available() > 0) { // if data available from reader 
val = mySerial.read();
if(val != 255){
Serial.print("4th:");
Serial.println(val, HEX);
}
} 

delay(500); // wait for a 1/2 second 
}

