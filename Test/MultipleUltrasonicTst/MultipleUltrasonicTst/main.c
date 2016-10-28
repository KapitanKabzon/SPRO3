/*
 * main.c
 *
 * Created: 24/10/2016 14:35:45
 *  Author: Piotr Chromi?ski
 *  Edited by: Catherine Beryl Basson
 */ 
#define F_CPU 16E6

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include <stdint.h>
#include <util/delay.h>
#include <inttypes.h>
#include "usart.h"

/* #define for trigger pin, for echo pin and registers, and for total number
 * of sensors */
#define TRIGGER PB0
#define ECHO0 PD2
#define ECHO0_REG PCINT18
#define ECHO1 PD3
#define ECHO1_REG PCINT19
#define ECHO2 PD4
#define ECHO2_REG PCINT20
#define SENSORS 3

/* #define for max number of clock cycles before max distance, and the time
 * duration in microseconds of one clock cycle */
#define MAX_PING 376183
#define US_PER_CLK 0.
void sensor_init(void);
void interrupt_init(void);
void interrupt_echo_enable(void);
void interrupt_echo_disable(void);
float get_distance(void);

volatile int flag = 0;
volatile uint32_t count = 0;
volatile char sensor[] = {ECHO0, ECHO1, ECHO2};
volatile char sensor_reg[] = {ECHO0_REG, ECHO1_REG, ECHO2_REG};
volatile int current_sensor = 0;

int main(void)
{
	uart_init();
	io_redirect();
	sensor_init();
	interrupt_init();
	
	float distance[SENSORS] = {0.00};
	
	while (1){
		distance[current_sensor] = get_distance();
		printf("Sensor %d: %.2f\n", current_sensor, distance[current_sensor]);
		current_sensor++;
		
		if (current_sensor > (SENSORS - 1))
			//printf("\n");
			current_sensor = 0;
		_delay_us(1000000);
	}
}

void sensor_init(void)
{
	/* Sets trigger as output, and clears so it outputs nothing */
	DDRB |= _BV(TRIGGER);		
	PORTB &= ~(_BV(TRIGGER));
	
	/* Sets ECHO pins as input */
	DDRD &= ~(_BV(ECHO0));
	DDRD &= ~(_BV(ECHO1));
}

void interrupt_init(void)
{
	/* Set PCIE2 to enable PCMSK2 scan (PD0 - PD7) */
	PCICR |= _BV(PCIE2);
}

float get_distance(void)
{
	interrupt_echo_enable();
	PORTB &= ~(_BV(TRIGGER));
	sei();
	
	/* Send a pulse */
	_delay_us(20);
	PORTB |= _BV(TRIGGER);
	_delay_us(12);
	PORTB &= ~(_BV(TRIGGER));
	
	/* Wait until echo is done receiving pulse */
	flag = 1;
 	while (flag);
		 
	/* Disable echo pin from reading */
	cli();
	interrupt_echo_disable();

	/* Check that maximum number of clock cycles hasn't been exceeded */
	if (count > MAX_PING || count == 0)
		count = MAX_PING;
	
	float dist = (double) count * US_PER_CLK / 58.275; /* pulse width time / ((microseconds per centimetre for speed of sound) * 2) */ 
	count = 0;
	return dist;
}

void interrupt_echo_enable(void)
{
	/* Trigger interrupt on level change */
	PCMSK2 |= _BV(sensor_reg[current_sensor]);
}

void interrupt_echo_disable(void)
{
	/* Disable interrupt for pin */
	PCMSK2 &= ~(_BV(sensor_reg[current_sensor]));
}

ISR (PCINT2_vect)
{
	if ((PIND & _BV(sensor[current_sensor]))) {
		/* Set up and start TIMER0 when echo receives pulse*/
		TIMSK0 |= (1 << TOIE0);
		TCCR0B |= _BV(CS00);
	} else {
		/* Stop timer and reset flag when pulse is done */
		TCCR0B &= ~(_BV(CS00));
		TIMSK0 &= ~(_BV(TOIE0));
		count += TCNT0;
		TCNT0 = 0;
		flag = 0;
	}
}

ISR (TIMER0_OVF_vect)
{
	/* Increase counter at every overflow */
	count += 255;
	
	if (count > MAX_PING){
		flag = 0;
		TCCR0B &= ~(_BV(CS00));
		TIMSK0 &= ~(_BV(TOIE0));
		count += TCNT0;
		TCNT0 = 0;
	}
}