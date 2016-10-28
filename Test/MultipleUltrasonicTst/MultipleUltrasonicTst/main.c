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

void interrupt_echo_enable(void);
void interrupt_echo_disable(void);
float get_distance(void);

volatile int flag = 0;
volatile int usart_check = 0;
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
	sei();
	
	float distance[SENSORS] = {0.00};
	
	while (1){
		distance[current_sensor] = get_distance();
		
		if (usart_check){
			for(int i = 0; i < SENSORS; i++){
				printf("Sensor %d: %.2f\n", i, distance[i]);
			}
			usart_check = 0;
		}
		
		current_sensor++;
		if (current_sensor > (SENSORS - 1))
			current_sensor = 0;
		_delay_ms(100);
	}
}

/* Interrupt service routines */
ISR (PCINT2_vect)
{
	if ((PIND & _BV(sensor[current_sensor]))) {
		/* Set up and start TIMER0 when echo receives pulse*/
		TIMSK0 |= _BV(TOIE0);
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


ISR (USART_RX_vect)
{
	if(UDR0)
		usart_check = 1;
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
	cli();
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
	sei();
	/* Check that maximum number of clock cycles hasn't been exceeded */
	if (count > MAX_PING || count == 0)
		count = MAX_PING;
	
	 /* pulse width time / ((microseconds per centimetre for speed of sound) * 2) */ 
	float dist = (double) count * US_PER_CLK / US_PER_CM_2;
	count = 0;
	
	return dist;
}

/* Trigger interrupt on level change for pin/register of current sensor */
void interrupt_echo_enable(void)
{
	PCMSK2 |= _BV(sensor_reg[current_sensor]);
}

/* Disables interrupt for pin/register of current sensor */
void interrupt_echo_disable(void)
{
	PCMSK2 &= ~(_BV(sensor_reg[current_sensor]));
}