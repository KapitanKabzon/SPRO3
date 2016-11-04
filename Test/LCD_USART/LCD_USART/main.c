/*
 * LCD_USART.c
 *
 * Created: 31/10/2016 13:08:52
 * Author : CatherineBeryl
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include <stdlib.h>
#include "usart.h"
#include "lcd.h"

volatile int i = 0;
volatile int data[10];
volatile char check;

int main(void)
{
    uart_init();
	io_redirect();
	lcd_init();
	sei();
	
	UCSR0B |= _BV(RXCIE0);
	
	printf("Hello world!");
	fprintf(&lcd_output, "Sup");
	while (1){
		if (check){
			printf("%d", *data);
			lcd_clear();
			lcd_gotoxy(1,1);
			fprintf(&lcd_output, "%d", *data);
			check = 0;
		}
	}
}

ISR (USART_RX_vect)

	check = 1;
}

