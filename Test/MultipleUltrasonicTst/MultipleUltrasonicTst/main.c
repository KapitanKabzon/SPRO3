/*
* main.c
*
* Created: 24/10/2016 14:35:45
*  Author: Piotr Chromi?ski
*  Edited by: Catherine Beryl Basson
*/
#define F_CPU 16000000UL

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
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

/* #define for the time duration in microseconds of one clock cycle,
* 2x microsecond per centimetre of speed of sound, max number of clock
* cycles before max distance */
#define US_PER_CLK 0.0625
#define US_PER_CM_2 58.275
#define MAX_PING ((400 * US_PER_CM_2) / US_PER_CLK)

/* Function prototypes */
/* Functions for initialisation */
void sensor_init(void);
void interrupt_init(void);

/* Functions to perform tasks */
float get_distance(void);

/* Modified by interrupts */
volatile int pulse_flag = 0;
volatile int usart_flag = 0;
volatile uint32_t count = 0;
volatile unsigned char data;

/* Not modified by interrupts, but read by them */
char sensor[] = {ECHO0, ECHO1, ECHO2};
char sensor_reg[] = {ECHO0_REG, ECHO1_REG, ECHO2_REG};
int sensor_id = 0;

int main(void)
{
	uart_init();
	io_redirect();
	sensor_init();
	interrupt_init();
	sei();
	
	float distance[SENSORS] = {0.00};
	
	while (1){
		distance[sensor_id] = get_distance();
		
		/* Send distance information over USART if usart_flag is set */
		if (usart_flag){
			for(int i = 0; i < SENSORS; i++){
				printf("%.2f, ",distance[i]);
			}
			printf("\n");
			usart_flag = 0;
		}
		
		/* Increase sensor_id to move onto the next sensor */
		sensor_id++;
		if (sensor_id > (SENSORS - 1))
			sensor_id = 0;
		_delay_ms(100);
	}
}

/* Interrupt service routines */
ISR (PCINT2_vect)
{
	if ((PIND & _BV(sensor[sensor_id]))) {
		/* Set up and start TIMER0 when echo receives pulse*/
		TIMSK0 |= _BV(TOIE0);
		TCCR0B |= _BV(CS00);
	} else {
		/* Stop timer and reset flag when pulse is done */
		TCCR0B &= ~(_BV(CS00));
		TIMSK0 &= ~(_BV(TOIE0));
		count += TCNT0;
		TCNT0 = 0;
		pulse_flag = 0;
	}
}

ISR (TIMER0_OVF_vect)
{
	/* Increase counter at every overflow */
	count += 255;
	
	/* Check that count hasn't exceeded maximum ping, and adjust */
	if (count > MAX_PING){
		TCCR0B &= ~(_BV(CS00));
		TIMSK0 &= ~(_BV(TOIE0));
		count += TCNT0;
		TCNT0 = 0;
		pulse_flag = 0;
	}
}


ISR (USART_RX_vect)
{
	/* Set usart flag to send distance info when call is received over USART */
	data = UDR0;
	usart_flag = 1;
}

/* Function definitions */
/* Initialise trigger and echo pins on the sensors */
void sensor_init(void)
{
	/* Sets trigger as output, and clears so it outputs nothing */
	DDRB |= _BV(TRIGGER);
	PORTB &= ~(_BV(TRIGGER));
	
	/* Sets ECHO pins as input */
	DDRD &= ~(_BV(ECHO0));
	DDRD &= ~(_BV(ECHO1));
	DDRD &= ~(_BV(ECHO2));
}

/* Initialise interrupt on pins PCINT[23:16] */
void interrupt_init(void)
{
	/* Set PCIE2 to enable PCMSK2 scan (PD0 - PD7) */
	PCICR |= _BV(PCIE2);
	
	/* Enable USART receive complete interrupt */
	UCSR0B |= _BV(RXCIE0);
}

/* Sends pulse through trigger and receives pulse width in echo, then
* calculates the distance and returns it to main() */
float get_distance(void)
{
	/* Make sure the trigger pin is set to low, and enable echo pin to trigger
	 * an interrupt */
	cli();
	PORTB &= ~(_BV(TRIGGER));
	PCMSK2 |= _BV(sensor_reg[sensor_id]);
	sei();
	
	/* Send a pulse */
	_delay_us(20);
	PORTB |= _BV(TRIGGER);
	_delay_us(12);
	PORTB &= ~(_BV(TRIGGER));
	
	/* Wait until echo is done receiving pulse */
	pulse_flag = 1;
	while (pulse_flag);
	
	/* Disable echo pin from triggering an interrupt */
	cli();
	PCMSK2 &= ~(_BV(sensor_reg[sensor_id]));
	sei();
	
	/* Check that maximum number of clock cycles hasn't been exceeded */
	if (count > MAX_PING || count == 0)
		count = MAX_PING;
	
	/* pulse width time / ((microseconds per centimetre for speed of sound) * 2) */
	float dist = (double) count * US_PER_CLK / US_PER_CM_2;
	count = 0;
	
	return dist;
}