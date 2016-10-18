/*
 * SDTest.c
 *
 * Created: 06/10/2016 10:42:12
 * Author : CatherineBeryl
 */ 

#define F_CPU 16E6;
#include <avr/io.h>
#include <stdio.h>
#include "diskio.h"
#include "usart.h"
#include "pff.h"

void errorHalt(char *msg);

FATFS fs;
const char MyFilenameStr[] = {"README.TXT"};

int main(void)
{	
	uint8_t buf[32];
	
	uart_init();
	io_redirect();
	
	disk_initialize();
	
	if (pf_mount(&fs))
		errorHalt("pf_mount");
		
	if (pf_open(MyFilenameStr))
		errorHalt("pf_open");
	
	while(1) {
		UINT nr;
		if(pf_read(buf, sizeof(buf), &nr))
			errorHalt("pf_read");
		if (nr == 0)
			break;
		
		printf("%d, %d", buf, nr);
	}
}

void errorHalt(char *msg)
{
	printf("Error: %s\n", msg);
}

