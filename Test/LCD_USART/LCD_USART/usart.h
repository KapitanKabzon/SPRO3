#ifndef USART_H_INCLUDED
#define USART_H_INCLUDED

extern FILE uart_output;
extern FILE uart_input;

void uart_putchar(char c, FILE *stream);
char uart_getchar(FILE *stream);

void uart_init(void);
void io_redirect(void);


#endif

