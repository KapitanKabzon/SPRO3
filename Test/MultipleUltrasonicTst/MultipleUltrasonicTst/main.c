/*
 * main.c
 *
 * Created: 24/10/2016 14:35:45
 *  Author: CatherineBeryl
 */ 
#define F_CPU 16E6

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include <stdint.h>
#include <util/delay.h>
#include "usart.h"

#define TRIGGER PB0
#define ECHO0 PD2
#define ECHO1 PD3

#define SENSORS 2
#define MAX_PING 376183

//void interrupt_init(void);
void sensor_init(void);
void interrupt_init(void);
float read_distance(void);

volatile int flag = 0;
volatile int wait = 1;
volatile uint32_t count = 0;
volatile char sensor[] = {ECHO0, ECHO1};
volatile int current_sensor = 0;

int main(void)
{
	uart_init();
	io_redirect();
	sensor_init();
	interrupt_init();
	
	float distance = 0.0;

	while (1){
		distance = read_distance();
		printf("Distance %d: %2f\n", current_sensor, distance);
		current_sensor++;
		if(current_sensor > (SENSORS - 1))
			current_sensor = 0;
		_delay_ms(1000);
	}
}

void sensor_init(void)
{
	DDRB |= _BV(TRIGGER);		// sets trigger as output
	PORTB &= ~(_BV(TRIGGER));	// clears trigger so it outputs nothing
	
	DDRD &= ~(_BV(ECHO0));		// sets ECHO1 as input
	DDRD &= ~(_BV(ECHO1));		// sets ECHO2 as input
}

void interrupt_init(void)
{
	PCICR |= _BV(PCIE2);					// set PCIE2 to enable PCMSK2 scan (PD0 - PD7)
	PCMSK2 |= _BV(PCINT18) | _BV(PCINT19);	// trigger interrupt on pin change for sensors
}

float read_distance(void)
{
	PORTB &= ~(_BV(TRIGGER));
	_delay_us(20);
	PORTB |= _BV(TRIGGER);
	_delay_us(12);
	PORTB &= ~(_BV(TRIGGER));
	sei();
	
	while(wait);
	while (flag) {
		count++;
		_delay_us(10);
	}
	
	if (count > MAX_PING || count == 0)
		count = MAX_PING;
		
	float distance = ((double) count / 1600000.0 * 17013.0);
	count = 0;
	cli();
	return distance;
}

ISR (PCINT2_vect)
{
	if ((PIND & _BV(sensor[current_sensor]))) {
		flag = 1;
		wait = 0;
	} else {
		flag = 0;
		wait = 1;
	}
}