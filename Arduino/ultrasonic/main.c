#define __AVR_ATmega328P__
#define F_CPU 16e6
#include <stdio.h>
#include <avr/io.h>
#include <stdint.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "usart.h"

#define MAX_PING 376183

void init_gpio(void);
void init_interrupt(void);
void wait16us(void);
void ping_init(void);
void ping_stop(void);
double ping_distance(void);

volatile uint32_t echo = 0;
volatile struct flags {
	unsigned int echo : 1;
	unsigned int ping_max : 1;
} flags;

int main(void)
{
	double distance = 0.0;
	flags.echo = 0;

	init_gpio();
	init_interrupt();
	io_redirect();
	uart_init();

	for (;;) {
		distance = ping_distance();
		printf("%f\n", distance);

		_delay_ms(70);
	}
    return 0;
}

ISR(INT0_vect)
{
	if (PIND & _BV(PD2)) {
		/* set up and start TIMER0 */
		TIMSK0 |= (1 << TOIE0);
		TCCR0B |= _BV(CS00);
	} else {
		/* stop timer and reset flag */
		TCCR0B &= ~(_BV(CS00));
		TIMSK0 &= ~(_BV(TOIE0));
		echo += TCNT0;
		TCNT0 = 0;
		flags.echo = 0;
	}
}

ISR(TIMER0_OVF_vect)
{
	echo += 255;

	/* check if out of range */
	if (echo > MAX_PING) {
		flags.echo = 0;
		TCCR0B &= ~(_BV(CS00));
		TIMSK0 &= ~(_BV(TOIE0));
		echo += TCNT0;
		TCNT0 = 0;
	}
}

void init_interrupt(void)
{
	/* INT0 trigger on any logical change */
    EICRA |= _BV(ISC00);
}

void init_gpio(void)
{
	/*
	 * ping sensor
	 * PD3 - trigger
	 * PD2 - echo (INT0)
	 */
    DDRD |= _BV(PD3);
	PORTD &= ~(_BV(PD3));
	DDRD &= ~(_BV(PD2));
}

double ping_distance(void)
{
	double distance = 0.0;
	cli();
	/* enable interrupt */
	EIMSK |= (_BV(INT0));
	/* send signal */
	PORTD &= ~(_BV(PD3));
	sei();

	/* send a pulse */
	_delay_us(20);
	PORTD |= _BV(PD3);
	_delay_us(12);
	PORTD &= ~(_BV(PD3));

	flags.echo = 1;

	/* get echo */
	while (flags.echo);

	/* disable interrupt */
	cli();
	EIMSK &= ~(_BV(INT0));
	sei();

	/* check for overflow and return distance */
	if (echo > MAX_PING || echo == 0)
		echo = MAX_PING;

	distance = (double) echo / 16000000 * 17013.0;
	echo = 0;

	return distance;
}
