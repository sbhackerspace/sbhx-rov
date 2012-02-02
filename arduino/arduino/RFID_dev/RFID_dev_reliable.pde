//Interface Arduino USB with Parallax 28440 125 Khz UART RFID Reader/Writer
//Program reads a EM4x50 tag and reports the ID on the serial monitor.
//Coded by Uberdude
//Modified by acf

#include "NewSoftSerial.h"
#include <EEPROM.h>
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
char ulist[256];
char s;

void initulist(){
        int i = 0;
        while(i != 255){
          ulist[i] = EEPROM.read(i);
          i++;
        }
        s = EEPROM.read(256);
}

uint8_t checkulist(char* c){
        //
        int i = 0;
        int d = 0;
        while(i != 4*(s) /*60*/){
         while(d != 4){
           //
           if(c[d] != ulist[i+d]) break;
           d++;
         }
         if(d == 4) return 0;
         i+=4; 
        }
        return 1;
}

void writeulist(char* c){
        int i = 0;
        while(i != 4){
          ulist[(s*4)+i] = c[i];
          EEPROM.write(s+i, c[i]);
          i++;
        }
        i = 0;
        s++;
        EEPROM.write(256, s);
        return; 
}

void setup() {
        int i = 0;
        
	Serial.begin(9600);
	mySerial.begin(9600);

        //EEPROM.write(0, 0);
        //EEPROM.write(1, 0);
        //EEPROM.write(256, 0);
        
        /*
        //Erase the entire EEPROM
        while(i != 256){
          EEPROM.write(i, 0);
          i++;
        }
        */
        
        
        
        /*
        EEPROM.write(0, 0x00);h
        EEPROM.write(1, 0xe7);
        EEPROM.write(2, 0x6c);
        EEPROM.write(3, 0x02);
        
        
        //Swiss's card
        EEPROM.write(4, 0x01);
        EEPROM.write(5, 0xe7);
        EEPROM.write(6, 0x6c);
        EEPROM.write(7, 0x02);
        */

	pinMode(txPin, OUTPUT); //pin 13
	pinMode(rxPin, INPUT); //pin 12
        pinMode(7, OUTPUT);
        pinMode(6, INPUT);
        digitalWrite(7, LOW);
        initulist();
        
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
                                                if(digitalRead(6) == 0) writeulist(&TAG1[0]);
                                                if(checkulist(&TAG1[0]) == 0) unlock();
                                                delay(1000);
                                                //unlock();
                        		}
                        	}

                        }
		}
	}
}


	
