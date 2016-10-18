#include <avr/io.h>
#include <stdio.h>
#include "usart.h"

#ifndef F_CPU
#define F_CPU 16000000UL
#endif

#ifndef BAUD
#define BAUD 9600
#endif
#include <util/setbaud.h>

//use uart_putchar and uart_getchar as the output to files
FILE uart_output = FDEV_SETUP_STREAM(uart_putchar, NULL, _FDEV_SETUP_WRITE);
FILE uart_input = FDEV_SETUP_STREAM(NULL, uart_getchar, _FDEV_SETUP_READ);


void uart_init(void) {

	/* setting up a clock signal for baud rate based on BAUD value */	
	UBRR0H = UBRRH_VALUE; // 0x00 
	UBRR0L = UBRRL_VALUE; // 0x67 for BAUD = 9600
	
	#if USE_2X
		UCSR0A |= _BV(U2X0);
	#else
		UCSR0A &= ~(_BV(U2X0));
	#endif

	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00); /* 8-bit data */
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);   /* Enable RX and TX */
}

void io_redirect(void){
		
		stdout = &uart_output;	//redirect standard output to uart
		stdin  = &uart_input;  //redirect standard input to uart
}
	

void uart_putchar(char c, FILE *stream) {
	if (c == '\n') {
		uart_putchar('\r', stream);
	}
	loop_until_bit_is_set(UCSR0A, UDRE0);
	UDR0 = c;
}

char uart_getchar(FILE *stream) {
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}
