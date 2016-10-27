/*
 * main.c
 *
 * Created: 24/10/2016 14:35:45
 *  Author: Piotr Chromi?ski
 *	Edited by: Catherine Beryl Basson
 */ 
#define F_CPU 16E6
#define US_PER_CLK 0.0625

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include <stdint.h>
#include <util/delay.h>
#include <inttypes.h>
#include "usart.h"

#define TRIGGER PB0			/* Trigger pin - Same for all sensors */
#define ECHO0 PD2			/* Echo pin for sensor 0 */
#define ECHO0_REG PCINT18	/* Echo register for sensor 0 (interrupt) */
#define ECHO1 PD3
#define ECHO1_REG PCINT19

#define SENSORS 2			/* Total number of sensors */
#define MAX_PING 376183		/* Max number of clock cycles to max distance */

void sensor_init(void);
void interrupt_init(void);
void interrupt_echo_enable(void);
void interrupt_echo_disable(void);
float get_distance(void);

volatile int flag = 0;
volatile uint32_t count = 0;
volatile char sensor[] = {ECHO0, ECHO1};
volatile char sensor_reg[] = {ECHO0_REG, ECHO1_REG};
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
			current_sensor = 0;
		_delay_us(1000000);
	}
}

void sensor_init(void)
{
	DDRB |= _BV(TRIGGER);		/* Sets trigger as output */
	PORTB &= ~(_BV(TRIGGER));	/* Clears trigger so it outputs nothing */
	
	DDRD &= ~(_BV(ECHO0));		/* Sets ECHO1 as input */
	DDRD &= ~(_BV(ECHO1));		/* Sets ECHO2 as input */
}

void interrupt_init(void)
{
	PCICR |= _BV(PCIE2);	/* Set PCIE2 to enable PCMSK2 scan (PD0 - PD7) */
}

void interrupt_echo_enable(void)
{
	PCMSK2 |= _BV(sensor_reg[current_sensor]);	/* Trigger interrupt on lvl change */
}

void interrupt_echo_disable(void)
{
	PCMSK2 &= ~(_BV(sensor_reg[current_sensor]));  /* Disable interrupt for pin */ 
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