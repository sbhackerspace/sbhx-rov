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
int i = 0;
//char code[6]; //Note this is 11 for the extra null char?
//int bytesread = 0;
//int flag = 0;

//Tags
char TAG1[5] = "";

void setup() {
	Serial.begin(9600);
	mySerial.begin(9600);

	pinMode(txPin, OUTPUT); //pin 13
	pinMode(rxPin, INPUT); //pin 12
        pinMode(7, OUTPUT);
        digitalWrite(7, LOW);
        
//        String thisString = String(13, BIN);
//        Serial.println(thisString);
//        if (thisString == "DFFEl.println("It equals");  

}

void loop() {
        read();
         }
void write() {
	mySerial.print("!RW");
	mySerial.print(RFID_WRITE, BYTE);
	mySerial.print(3, BYTE);
	mySerial.print(0xCC, BYTE);
	mySerial.print(0xCC, BYTE);
	mySerial.print(0xCC, BYTE);
	mySerial.print(0xCC, BYTE);

	//Error code read
	if (mySerial.available() > 0) { // if data available from reader 
		val = mySerial.read();
		if (val != 255) {
			Serial.print("Write Error Code:");
			Serial.println(val, HEX);
		}
	}

}

void unlock(){
    digitalWrite(7, HIGH);
    delay(300);
    digitalWrite(7,LOW);
}

void read() {
	mySerial.print("!RW");
	mySerial.print(RFID_READ, BYTE);
	mySerial.print(32, BYTE);

        while (!mySerial.available() > 0) {
          if (Serial.read() == 'U') {
            unlock();
        }
          
        }

	//0th read
	if (mySerial.available() > 0) { // if data available from reader 
		val = mySerial.read();
		if (val != 255) {
			if (val = 1){
                                //1st byte
                        	if (mySerial.available() > 0) { // if data available from reader 
                        		val = mySerial.read();
                        		if (val != 255 && val != 0) {
                        			//Serial.print("1st:");
                        			//Serial.println(val, HEX);
                                                TAG1[0] = val;
                        		}
                        	}
                        
                        	//2nd byte
                        	if (mySerial.available() > 0) { // if data available from reader 
                        		val = mySerial.read();
                        		if (val != 255 && val != 0) {
                        			//Serial.print("2nd:");
                        			//Serial.println(val, HEX);
                                                TAG1[1] = val;
                        		}
                        	}
                        
                        	//3rd byte
                        	if (mySerial.available() > 0) { // if data available from reader 
                        		val = mySerial.read();
                        		if (val != 255 && val != 0) {
                        			//Serial.print("3rd:");
                        			//Serial.println(val, HEX);
                                                TAG1[2] = val;
                        		}
                        	}
                        
                        	//4th byte
                        
                        	if (mySerial.available() > 0) { // if data available from reader 
                        		val = mySerial.read();
                        		if (val != 255 && val != 0) {
                        			//Serial.print("4th:");
                        			//Serial.println(val, HEX);
                                                //Serial.println("");
                                                TAG1[3] = val;
                                                TAG1[4] = '\0';
                                                Serial.println(TAG1);
                                                delay(1000);
                                                //unlock();
                        		}
                        	}

                        }
		}
	}
}


	
