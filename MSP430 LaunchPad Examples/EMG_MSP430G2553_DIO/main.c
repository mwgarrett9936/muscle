#include "msp430g2553.h"
#include <string.h>

	unsigned int ADC[5]; 		//Holds ADC values (ADC[0] = P1.4, ADC[4] = P1.0)
	unsigned int A0value = 0; 	//ADC value read on P1.0
	unsigned int A4value = 0; 	//ADC value read on P1.4
	unsigned int A0max = 0;
	unsigned int A0min = 1024;

void main(void)

{
	WDTCTL = WDTPW + WDTHOLD; 	//Disable WDT

	BCSCTL1 = CALBC1_1MHZ; 		// Set DCO
	DCOCTL = CALDCO_1MHZ;
	P1DIR |= BIT5;
	P2DIR |= BIT0 + BIT1 + BIT2;

	/* Start with A4 only, SMCLK, Conversion Sequence */
	ADC10CTL1 = INCH_4 + ADC10SSEL_1 + ADC10SSEL_0 + CONSEQ_1;
	/* Turn on ADC, Multiple Sample and Conversion,  Enable Interrupt */
	ADC10CTL0 = ADC10ON + MSC + ADC10IE;
	ADC10AE0 |= 0x11;        	// Enable A0 and A4 which are P1.0,P1.4
	ADC10DTC1 = 5;			   	// Five conversions in sequence only 2 are needed
	ADC10SA = (short)&ADC[0]; 	// ADC10 data transfer starting address.

	__bis_SR_register(GIE); 	// Enter LPM0, interrupts enabled
	while(1) {
		ADC10CTL0 |= ENC + ADC10SC;
		while (ADC10CTL1 & BUSY)
		if(A0value < A0min)
			A0min = A0value;
		if(A0value > A0max)
			A0max = A0value;
		if(A0value > 200) {
			P1OUT |= BIT5;
			if(A0value > 300)
				P2OUT |= BIT0;
			else
				P2OUT &= ~BIT0;
			if(A0value > 500)
				P2OUT |= BIT1;
			else
				P2OUT &= ~BIT1;
			if(A0value > 600)
				P2OUT |= BIT2;
			else
				P2OUT &= ~BIT2;
		}
		else {
			P1OUT &= ~BIT5;
			P2OUT &= ~BIT0;
			P2OUT &= ~BIT1;
			P2OUT &= ~BIT2;
		}


	}
}

#pragma vector=ADC10_VECTOR
__interrupt void ADC10_ISR (void) {
	A0value = ADC[4];  			// Index is reversed
	A4value = ADC[0];
	ADC10CTL0 &= ~ADC10IFG;  	// clear interrupt flag
	ADC10SA = (short)&ADC[0]; 	// ADC10 data transfer starting address.
}

