#include <MD25.h>


byte inByte;

MD25 test(88);
void setup(){
  Serial.begin(9600);
  
  //byte test = 193;
  
  //Serial.println(test, BIN);
 // parseSerial(test);
}

void loop(){
  if (Serial.available() > 0){
    inByte = Serial.read();
    parseSerial(inByte);
  }
}


void parseSerial(byte inByte){
  byte motor;
  byte speed;
  byte controller;
  
  //Serial.print(inByte);
  //Serial.print(":");
  //Serial.println(inByte, BIN);
  
  controller = (inByte & 0b11000000) >> 6;
  motor = (inByte & 0b00100000) >> 5;
  speed = (inByte & 0b00011111);
  
  test.changeSpeed(controller, motor, speed);
  //test.stopMotor();

  Serial.print("Motor #:");
  Serial.println(motor, DEC);
  Serial.print("Motor Speed:");
  Serial.println(speed, DEC);
  Serial.print("Controller #:");
  Serial.println(controller, DEC);  
}


