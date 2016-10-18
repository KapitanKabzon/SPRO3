/*-----------------------------------------------------------------------
/  PFF - Low level disk interface modlue include file    (C)ChaN, 2009
/-----------------------------------------------------------------------*/

#ifndef _DISKIO

#include "integer.h"
#include <avr/io.h>

/* Definitions for SPI pins on ATMega328P */
#define CS (_BV(PB2))
#define MOSI (_BV(PB3))
#define MISO (_BV(PB4))
#define SCK (_BV(PB5))

/* Status of Disk Functions */
typedef BYTE	DSTATUS;


/* Results of Disk Functions */
typedef enum {
	RES_OK = 0,		/* 0: Function succeeded */
	RES_ERROR,		/* 1: Disk error */
	RES_STRERR,		/* 2: Seream error */
	RES_NOTRDY,		/* 3: Not ready */
	RES_PARERR		/* 4: Invalid parameter */
} DRESULT;


/*---------------------------------------*/
/* Prototypes for disk control functions */

DSTATUS disk_initialize (void);
DRESULT disk_readp (BYTE *, DWORD, WORD, WORD);
uint8_t rcv_spi(void);
uint8_t xmit_spi(uint8_t byte);
void spi_init(void);
DRESULT disk_writep (const BYTE *buff, DWORD sa);

#define STA_NOINIT		0x01	/* Drive not initialized */
#define STA_NODISK		0x02	/* No medium in the drive */

/* Card type flags (CardType) */
#define CT_MMC				0x01	/* MMC ver 3 */
#define CT_SD1				0x02	/* SD ver 1 */
#define CT_SD2				0x04	/* SD ver 2 */
#define CT_SDC				(CT_SD1|CT_SD2)	/* SD */
#define CT_BLOCK			0x08	/* Block addressing */

#define _DISKIO
#endif