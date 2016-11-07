/*
 * LCD_USART.c
 *
 * Created: 31/10/2016 13:08:52
 * Author : CatherineBeryl
 */ 
#define F_CPU 16E6

#define B0 0x3E // DI_0 button pressed
#define B1 0x3D // DI_1
#define B2 0x3B // DI_2
#define B3 0x37 // DI_3

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "usart.h"
#include "lcd.h"

void ioboard_config(void);

volatile char data[10];
volatile char check;
int roomnr;

int main(void)
{
    ioboard_config();
	uart_init();
	io_redirect();
	lcd_init();
	sei();
	
	UCSR0B |= _BV(RXCIE0);
	
	printf("Hello world!");
	fprintf(&lcd_output, "Sup");
	while (1){
		if (check){
			strtok(data, "\n\r");
			roomnr = atoi(data);
			printf("%d\n", roomnr);
			lcd_clear();
			lcd_gotoxy(1,1);
			fprintf(&lcd_output, "%d", roomnr);
			check = 0;
		}
	}
}

ISR (USART_RX_vect)
{
	fgets(data, 10, stdin);
	check = UDR0;
	check = 1;
}

void ioboard_config (void)
{
	DDRC = 0xF0; // buttons as inputs
	PORTC = 0x3F; //Internal pull at PC0-3
}
