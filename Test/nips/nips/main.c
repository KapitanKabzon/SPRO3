/*
 * EMB2Exam.c
 *
 * Created: 2016-05-11
 * Author : Catherine Beryl Basson
 */ 

#define F_CPU 16000000UL

#include <avr/io.h>
#include <avr/interrupt.h>

#define BAUDRATE 9600 // using a baudrate of 9600
#define BAUDRATE_PRESCALER (((F_CPU / (BAUDRATE * 16UL))) - 1) // calculates the baudrate prescaler

/* function prototypes */
void ioboard_config(void); // configures the digital IO board
void usart_init(void); // to initialise USART
void usart_send(unsigned char data); // to send a value on the usart
unsigned char usart_receive(void); // to receive a value on the usart

int main(void)
{
	ioboard_config(); // configures buttons and leds on IO board
	usart_init(); // initialises USART
}	

/* interrupt service routines */
ISR (TIMER0_COMPA_vect) // interrupt service routine for timer 0
{
		
}

ISR (PCINT1_vect) // interrupt service routine for push of a button
{
	
}

/* function definitions */
void ioboard_config(void) // configures the buttons as inputs, and the leds as outputs
{
	DDRC = 0xF0; //PC 0-3 as inputs
	PORTC = 0x3F; //Internal pull at PC0-3 !!! PINC = BUTTON !!! 0 for button pushed on last nibble
	DDRD = 0xFF;  //PD 4-7 as outputs PORTD = LIGHT 1 for light on on first nibble
	PORTD = 0x00; //Output LEDs off
}

void usart_init(void)
{
	UBRR0H = (uint8_t) (BAUDRATE_PRESCALER >> 8); // sets high byte registers
	UBRR0L = (uint8_t) BAUDRATE_PRESCALER; // sets low byte registers
	UCSR0B = _BV(RXEN0) | _BV(TXEN0); // enables RX and TX pins
	UCSR0C = (_BV(UCSZ00) | _BV(UCSZ01)); //configures 1 stop bit, data length 8, and no parity
}

void usart_send(unsigned char data) // checks register A to see if there is data to be received
{
	while(!(UCSR0A & _BV(UDRE0))); // waits for transmit buffer
	UDR0 = data; // data to be sent
}

unsigned char usart_receive(void) // checks register A to see if there is data to be received
{
	while(!(UCSR0A & _BV(RXC0))); // waits for new data
	return UDR0; // returns the received data
}

/* ENABLE BUTTONS FOR INTERRUPT */
/*
PCICR |= _BV(PCIE1); // set PCIE1 to enable PCMSK1 scan
PCMSK1 |=  _BV(PCINT8) | _BV(PCINT9) | _BV(PCINT10) | _BV(PCINT11); // set PCINT10 to trigger an interrupt on state change - button DI0, DI1, DI2 and DI3
*/

/* TIMER0 FOR ONE MILISECOND - INTERRUPT */
/*
TCCR0A |= _BV(WGM01); // set the timer mode to CTC
OCR0A = 0xF9; // sets value that we would like to count to (for compare)
TIMSK0 |= _BV(OCIE0A);    // sets the ISR COMPA vect

sei(); // enables interrupts
TCCR0B |= _BV(CS01) | _BV(CS00); // sets prescaler to 64 and start the timer


USED IN DELAY(while ((TIFR0 & _BV(OCF0A)) == 0); // waits for overflow event
TIFR0 = _BV(OCF0A); // resets overflow flag)
*/

/*
DDRB |= _BV(DDB5); // sets heartbeat light as output
PORTB ^=0xFF; // toggles heartbeat LED	
*/

/* ADC CONVERSION */
/* ADCSRA |= _BV(ADEN) | _BV(ADPS1); // enables ADC and sets prescaler to 2

uint16_t adc_read(uint8_t adcx)
{
	ADMUX = _BV(REFS0); // sets AVcc as the reference voltage
	
	ADMUX &= 0xf0; // sets AMUX to its higher four bits
	ADMUX |= adcx; // selects PCO as the analogue pin we would like to use
	
	ADCSRA |= _BV(ADSC); // starts the conversion
	
	while((ADCSRA & _BV(ADSC))); // this loops until the conversion is finished
	
	return ADC; // returns the converted value to main
}

#include <stdint>
#define ADC_PIN 0
*/