/*
 * attiny2313blink.c
 *
 * Created: 8/6/2011 6:49:39 PM
 *  Author: Mike
 */ 

#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
	DDRB = 0xFF;
	PORTB = 0x00;
    while(1)
    {
		while(PORTB <= 0xFF){
			_delay_loop_2(0);
			PORTB++;
		}
		_delay_loop_2(0);
		PORTB=0x00;
			
    }
}