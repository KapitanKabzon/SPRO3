/*-------------------------------------------------------------------------/
/  Stand-alone MMC boot loader  R0.01
/--------------------------------------------------------------------------/
/
/  Copyright (C) 2010, ChaN, all right reserved.
/
/ * This software is a free software and there is NO WARRANTY.
/ * No restriction on use. You can use, modify and redistribute it for
/   personal, non-profit or commercial products UNDER YOUR RESPONSIBILITY.
/ * Redistributions of source code must retain the above copyright notice.
/
/--------------------------------------------------------------------------/
/ Dec 6, 2010  R0.01  First release
/--------------------------------------------------------------------------/
/ This is a stand-alone MMC/SD boot loader for megaAVRs. It requires a 4KB
/ boot section for code, four GPIO pins for MMC/SD as shown in sch.jpg and
/ nothing else. To port the boot loader into your project, follow the
/ instruction sdescribed below.
/
/ 1. Setup the hardware. Attach a memory card socket to the any GPIO port
/    where you like. Select boot size at least 4KB for the boot loader with
/    BOOTSZ fuses and enable boot loader with BOOTRST fuse.
/
/ 2. Setup the software. Change the four port definitions in the asmfunc.S.
/    Change MCU_TARGET, BOOT_ADR and MCU_FREQ in the Makefile. The BOOT_ADR
/    is a BYTE address of boot section in the flash. Build the boot loader
/    and write it to the device with a programmer.
/
/ 3. Build the application program and output it in binary form instead of
/    hex format. Rename the file "app.bin" and put it into the memory card.
/
/ 4. Insert the card and turn the target power on. When the boot loader found
/    the application file, the file is written into the flash memory prior to
/    start the application program. On-board LED lights (if exist) during
/    the flash programming operation.
/
/-------------------------------------------------------------------------*/


#include <avr/io.h>
#include "pff.h"
#include "usart.h"


void errorHalt(char *msg);

FATFS fs;
const char MyFilenameStr[] = {"README.TXT"};

int main(void)
{
	uint8_t buf[32];
	
	uart_init();
	io_redirect();
	
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

