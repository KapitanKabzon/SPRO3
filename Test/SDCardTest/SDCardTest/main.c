/*
 * SDCardTest.c
 *
 * Created: YYYY-MM-DD HH:MM:SS
 * Author : Catherine Beryl
 */ 

#define F_CPU 16E6

#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>
#include "ff.h"
#include "diskio.h"

int main(void)
{
	FRESULT f_error_code;
	static FATFS FATFS_Obj;
	
	disk_initialize(0);
	f_error_code = f_mount(0, FATFS_Obj, 1);
	
	FIL fil_obj;
	int x = 5;
	f_open(&fil_obj, "/test/tst.txt", FA_WRITE);
	f_printf(&fil_obj, "five: %d", x);
	f_close(&fil_obj);
}

