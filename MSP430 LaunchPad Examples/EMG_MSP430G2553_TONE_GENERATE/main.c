/******************************************************************************
 *
 * TI FlexPack - MSP430 LaunchPad Tone/PWM Generator Demo
 *
 * This example uses both inputs of the TI FlexPack booster pack to control
 * the frequency of a PWM signal on pin P1.2. Input channel 1 determines
 * whether or not the the PWM signal will be generated.  Input channel 2
 * determines the frequency of the PWM signal.  The greater the voltage
 * received from input 1 will result in a higher frequency.
 *
 *****************************************************************************/
#include "msp430g2553.h"

	unsigned int ADC[5]; 		//Holds ADC values (ADC[0] = P1.4, ADC[4] = P1.0)
	unsigned int A0value = 0; 	//ADC value read on P1.0
	unsigned int A4value = 0; 	//ADC value read on P1.4

void tone(int freq)  // Freq = SMCLK/CCR0; SMCLK = 1MHz
{

	CCR0=1000000/freq;      //Calculate CCR0
	CCR1=CCR0/2;    //50% Duty Cycle
}

void notone(void)
{

	CCR0=0;
}

void main(void)

 {
	WDTCTL = WDTPW + WDTHOLD; 	//Disable WDT

	BCSCTL1 = CALBC1_1MHZ; 		// Set DCO
	DCOCTL = CALDCO_1MHZ;

	/* Start with A4 only, SMCLK, Conversion Sequence */
	ADC10CTL1 = INCH_4 + ADC10SSEL_1 + ADC10SSEL_0 + CONSEQ_1;
	/* Turn on ADC, Multiple Sample and Conversion,  Enable Interrupt */
	ADC10CTL0 = ADC10ON + MSC + ADC10IE;
	ADC10AE0 |= 0x11;        	// Enable A0 and A4 which are P1.0,P1.4
	ADC10DTC1 = 5;			   	// Five conversions in sequence only 2 are needed
	ADC10SA = (short)&ADC[0]; 	// ADC10 data transfer starting address.
	P1DIR |= 0x04;                            // P1.2 output
	P1SEL |= 0x04;                            // P1.2 TA1/2 options
	//CCR0 = 512-1;                             // PWM Period
	CCTL1 = OUTMOD_7;                         // CCR1 reset/set
	//CCR1 = 384;                               // CCR1 PWM duty cycle
	TACTL = TASSEL_2 + MC_1;                  // SMCLK, up mode
	__bis_SR_register(GIE); 	// Enter LPM0, interrupts enabled
	while(1) {
		ADC10CTL0 |= ENC + ADC10SC;
		while (ADC10CTL1 & BUSY);
		//__delay_cycles(1000);
		int offset = -100;
		if(A0value > 200) {
			if(A4value < 300)
				tone(300+offset);
			else if(A4value < 400 && A4value > 300)
				tone(400+offset);
			else if(A4value < 500 && A4value > 400)
				tone(500+offset);
			else if(A4value < 600 && A4value > 500)
				tone(600+offset);
			else if(A4value < 700 && A4value > 600)
				tone(700+offset);
			else if(A4value < 800 && A4value > 700)
				tone(800+offset);
			else if(A4value < 900 && A4value > 800)
				tone(900+offset);
			else if(A4value < 1000 && A4value > 900)
				tone(1000+offset);
		} else
			notone();
	}
}

#pragma vector=ADC10_VECTOR
__interrupt void ADC10_ISR (void) {
	A0value = ADC[4];  			// Index is reversed
	A4value = ADC[0];
	ADC10CTL0 &= ~ADC10IFG;  	// clear interrupt flag
	ADC10SA = (short)&ADC[0]; 	// ADC10 data transfer starting address.
}

#pragma vector=TIMER0_A0_VECTOR
__interrupt void ta0_isr(void)
{
  TACTL = 0;
  LPM0_EXIT;                                // Exit LPM0 on return
}

