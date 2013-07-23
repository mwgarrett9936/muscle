#include "msp430g2553.h"
#include <string.h>

	unsigned int ADC[5]; 		//Holds ADC values (ADC[0] = P1.4, ADC[4] = P1.0)
	unsigned int A0value = 0; 	//ADC value read on P1.0
	unsigned int A4value = 0; 	//ADC value read on P1.4

	char value[4]; 				//Stores string to be sent via UART

void uart_putc(unsigned char c) {
	while (!(IFG2&UCA0TXIFG));	// USCI_A0 TX buffer ready?
  	UCA0TXBUF = c;            	// TX
}

void uart_puts(const char *str) {
     while(*str) uart_putc(*str++);
}

/* reverse:  reverse string s in place */
void reverse(char s[])
{
    int i, j;
    char c;

    for (i = 0, j = strlen(s)-1; i<j; i++, j--) {
        c = s[i];
        s[i] = s[j];
        s[j] = c;
    }
}

void itoa(int n, char s[])
{
    int i, sign;

    if ((sign = n) < 0)  /* record sign */
        n = -n;          /* make n positive */
    i = 0;
    do {       /* generate digits in reverse order */
        s[i++] = n % 10 + '0';   /* get next digit */
    } while ((n /= 10) > 0);     /* delete it */
    if (sign < 0)
        s[i++] = '-';
    s[i] = '\0';
    reverse(s);
}

void main(void)

{
	WDTCTL = WDTPW + WDTHOLD; 	//Disable WDT

	BCSCTL1 = CALBC1_1MHZ; 		// Set DCO
	DCOCTL = CALDCO_1MHZ;
	P1SEL = BIT2 ; 				// P1.2=TXD
	P1SEL2 = BIT2 ; 			// P1.2=TXD

	/* Start with A4 only, SMCLK, Conversion Sequence */
	ADC10CTL1 = INCH_4 + ADC10SSEL_1 + ADC10SSEL_0 + CONSEQ_1;
	/* Turn on ADC, Multiple Sample and Conversion,  Enable Interrupt */
	ADC10CTL0 = ADC10ON + MSC + ADC10IE;
	ADC10AE0 |= 0x11;        	// Enable A0 and A4 which are P1.0,P1.4
	ADC10DTC1 = 5;			   	// Five conversions in sequence only 2 are needed
	ADC10SA = (short)&ADC[0]; 	// ADC10 data transfer starting address.

	UCA0CTL1 |= UCSSEL_2; 		// SMCLK
	UCA0BR0 = 104; 				// 1MHz 9600
	UCA0BR1 = 0; 				// 1MHz 9600
	UCA0MCTL = UCBRS0; 			// Modulation UCBRSx = 1
	UCA0CTL1 &= ~UCSWRST; 		// Initialize USCI state machine
	__bis_SR_register(GIE); 	// Enter LPM0, interrupts enabled
	for (;;)
	  {
		ADC10CTL0 |= ENC + ADC10SC;
		uart_puts("A0 = ");
		itoa(A0value, value);
		uart_puts(value);
		uart_puts(" - ");
		while (ADC10CTL1 & BUSY);
		uart_puts("A4 = ");
		itoa(A4value, value);
		uart_puts(value);
		uart_putc(0x0D); 		//Carriage return \r
		uart_putc(0x0A); 		//Line feed \n
	  }
}

#pragma vector=ADC10_VECTOR
__interrupt void ADC10_ISR (void) {
	A0value = ADC[4];  			// Index is reversed
	A4value = ADC[0];
	ADC10CTL0 &= ~ADC10IFG;  	// clear interrupt flag
	ADC10SA = (short)&ADC[0]; 	// ADC10 data transfer starting address.
}
