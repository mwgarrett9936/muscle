//#############################################################################
//
//  File:   f2802x_examples_ccsv4/adc_soc/Example_F2802xAdcSoc.c
//
//  Title:  F2802x ADC Start-Of-Conversion (SOC) Example Program.
//
//  Group:          C2000
//  Target Device:  TMS320F2802x
//
//! \addtogroup example_list
//!  <h1>ADC Start-Of-Conversion (SOC)</h1>
//!
//!   Interrupts are enabled and the ePWM1 is setup to generate a periodic
//!   ADC SOC - ADCINT1. Two channels are converted, ADCINA4 and ADCINA2.
//!
//!   Watch Variables:
//!
//!   - Voltage1[10] - Last 10 ADCRESULT0 values
//!   - Voltage2[10] - Last 10 ADCRESULT1 values
//!   - ConversionCount - Current result number 0-9
//!   - LoopCount - Idle loop counter
//
//  (C) Copyright 2012, Texas Instruments, Inc.
//#############################################################################
// $TI Release: LaunchPad f2802x Support Library v100 $
// $Release Date: Wed Jul 25 10:45:39 CDT 2012 $
//#############################################################################

#include "DSP28x_Project.h"     // Device Headerfile and Examples Include File

#include "f2802x_common/include/adc.h"
#include "f2802x_common/include/clk.h"
#include "f2802x_common/include/flash.h"
#include "f2802x_common/include/gpio.h"
#include "f2802x_common/include/pie.h"
#include "f2802x_common/include/pll.h"
#include "f2802x_common/include/wdog.h"

//#define HIGH_THRESHOLD 500
//#define MID_THRESHOLD 200

//#define HIGH_THRESHOLD2 500 Uncomment and change above to xxx_THRESHOLD1 if there are different offsets
//#define MID_THRESHOLD2 200  Uncomment and change above to xxx_THRESHOLD1 if there are different offsets

// Prototype statements for functions found within this file.
interrupt void adc_isr(void);
void Adc_Config(void);

//Global Variables Used To Store ADC Results
uint16_t Sig1_Voltage;
uint16_t Sig2_Voltage;

//Threshold Values for State Changes
uint16_t high1;
uint16_t mid1;
uint16_t high2;
uint16_t mid2;

ADC_Handle myAdc;
CLK_Handle myClk;
FLASH_Handle myFlash;
GPIO_Handle myGpio;
PIE_Handle myPie;
PWM_Handle myPwm;

void main(void)
{
    
    CPU_Handle myCpu;
    PLL_Handle myPll;
    WDOG_Handle myWDog;
    
    high1 = 500;
    mid1 = 200;
    high2 = 500;
    mid2 = 200;

    // Initialize all the handles needed for this application    
    myAdc = ADC_init((void *)ADC_BASE_ADDR, sizeof(ADC_Obj));
    myClk = CLK_init((void *)CLK_BASE_ADDR, sizeof(CLK_Obj));
    myCpu = CPU_init((void *)NULL, sizeof(CPU_Obj));
    myFlash = FLASH_init((void *)FLASH_BASE_ADDR, sizeof(FLASH_Obj));
    myGpio = GPIO_init((void *)GPIO_BASE_ADDR, sizeof(GPIO_Obj));
    myPie = PIE_init((void *)PIE_BASE_ADDR, sizeof(PIE_Obj));
    myPll = PLL_init((void *)PLL_BASE_ADDR, sizeof(PLL_Obj));
    myPwm = PWM_init((void *)PWM_ePWM1_BASE_ADDR, sizeof(PWM_Obj));
    myWDog = WDOG_init((void *)WDOG_BASE_ADDR, sizeof(WDOG_Obj));
    myGpio = GPIO_init((void *)GPIO_BASE_ADDR, sizeof(GPIO_Obj));

    // Perform basic system initialization    
    WDOG_disable(myWDog);
    CLK_enableAdcClock(myClk);
    (*Device_cal)();
    
    //Select the internal oscillator 1 as the clock source
    CLK_setOscSrc(myClk, CLK_OscSrc_Internal);
    
    // Setup the PLL for x10 /2 which will yield 50Mhz = 10Mhz * 10 / 2
    PLL_setup(myPll, PLL_Multiplier_10, PLL_DivideSelect_ClkIn_by_2);
    
    // Disable the PIE and all interrupts
    PIE_disable(myPie);
    PIE_disableAllInts(myPie);
    CPU_disableGlobalInts(myCpu);
    CPU_clearIntFlags(myCpu);
    
// If running from flash copy RAM only functions to RAM   
#ifdef _FLASH
    memcpy(&RamfuncsRunStart, &RamfuncsLoadStart, (size_t)&RamfuncsLoadSize);
#endif   

    // Setup a debug vector table and enable the PIE
    PIE_setDebugIntVectorTable(myPie);
    PIE_enable(myPie);

    // Register interrupt handlers in the PIE vector table
    PIE_registerPieIntHandler(myPie, PIE_GroupNumber_10, PIE_SubGroupNumber_1, (intVec_t)&adc_isr);

    // Enable an GPIO output on GPIO28, GPIO29, GPIO 34, and GPIO18, set them high
    GPIO_setPullUp(myGpio, GPIO_Number_28, GPIO_PullUp_Enable);
    GPIO_setHigh(myGpio, GPIO_Number_28);
    GPIO_setMode(myGpio, GPIO_Number_28, GPIO_6_Mode_GeneralPurpose);
    GPIO_setDirection(myGpio, GPIO_Number_28, GPIO_Direction_Output);

    GPIO_setPullUp(myGpio, GPIO_Number_29, GPIO_PullUp_Enable);
    GPIO_setHigh(myGpio, GPIO_Number_29);
    GPIO_setMode(myGpio, GPIO_Number_29, GPIO_6_Mode_GeneralPurpose);
    GPIO_setDirection(myGpio, GPIO_Number_29, GPIO_Direction_Output);

    GPIO_setPullUp(myGpio, GPIO_Number_34, GPIO_PullUp_Enable);
    GPIO_setHigh(myGpio, GPIO_Number_34);
    GPIO_setMode(myGpio, GPIO_Number_34, GPIO_6_Mode_GeneralPurpose);
    GPIO_setDirection(myGpio, GPIO_Number_34, GPIO_Direction_Output);

    GPIO_setPullUp(myGpio, GPIO_Number_18, GPIO_PullUp_Enable);
    GPIO_setHigh(myGpio, GPIO_Number_18);
    GPIO_setMode(myGpio, GPIO_Number_18, GPIO_6_Mode_GeneralPurpose);
    GPIO_setDirection(myGpio, GPIO_Number_18, GPIO_Direction_Output);

    //Enable gpios as PWM1
    GPIO_setMode(myGpio, GPIO_Number_0, GPIO_0_Mode_EPWM1A);
    GPIO_setMode(myGpio, GPIO_Number_1, GPIO_1_Mode_EPWM1B);

    // Initialize the ADC
    ADC_enableBandGap(myAdc);
    ADC_enableRefBuffers(myAdc);
    ADC_powerUp(myAdc);
    ADC_enable(myAdc);
    ADC_setVoltRefSrc(myAdc, ADC_VoltageRefSrc_Int);

    // Enable ADCINT1 in PIE
    PIE_enableAdcInt(myPie, ADC_IntNumber_1);
    // Enable CPU Interrupt 1
    CPU_enableInt(myCpu, CPU_IntNumber_10);
    // Enable Global interrupt INTM
    CPU_enableGlobalInts(myCpu);
    // Enable Global realtime interrupt DBGM
    CPU_enableDebugInt(myCpu);

    // Configure ADC
    //Note: Channel ADCINA4  will be double sampled to workaround the ADC 1st sample issue for rev0 silicon errata  
    ADC_setIntPulseGenMode(myAdc, ADC_IntPulseGenMode_Prior);               //ADCINT1 trips after AdcResults latch
    ADC_enableInt(myAdc, ADC_IntNumber_1);                                  //Enabled ADCINT1
    ADC_setIntMode(myAdc, ADC_IntNumber_1, ADC_IntMode_ClearFlag);          //Disable ADCINT1 Continuous mode
    ADC_setIntSrc(myAdc, ADC_IntNumber_1, ADC_IntSrc_EOC2);                 //setup EOC2 to trigger ADCINT1 to fire
    ADC_setSocChanNumber (myAdc, ADC_SocNumber_0, ADC_SocChanNumber_A4);    //set SOC0 channel select to ADCINA4
    ADC_setSocChanNumber (myAdc, ADC_SocNumber_1, ADC_SocChanNumber_A4);    //set SOC1 channel select to ADCINA4
    ADC_setSocChanNumber (myAdc, ADC_SocNumber_2, ADC_SocChanNumber_A6);    //set SOC2 channel select to ADCINA2
    ADC_setSocTrigSrc(myAdc, ADC_SocNumber_0, ADC_SocTrigSrc_EPWM1_ADCSOCA);    //set SOC0 start trigger on EPWM1A, due to round-robin SOC0 converts first then SOC1
    ADC_setSocTrigSrc(myAdc, ADC_SocNumber_1, ADC_SocTrigSrc_EPWM1_ADCSOCA);    //set SOC1 start trigger on EPWM1A, due to round-robin SOC0 converts first then SOC1
    ADC_setSocTrigSrc(myAdc, ADC_SocNumber_2, ADC_SocTrigSrc_EPWM1_ADCSOCA);    //set SOC2 start trigger on EPWM1A, due to round-robin SOC0 converts first then SOC1, then SOC2
    ADC_setSocSampleWindow(myAdc, ADC_SocNumber_0, ADC_SocSampleWindow_7_cycles);   //set SOC0 S/H Window to 7 ADC Clock Cycles, (6 ACQPS plus 1)
    ADC_setSocSampleWindow(myAdc, ADC_SocNumber_1, ADC_SocSampleWindow_7_cycles);   //set SOC1 S/H Window to 7 ADC Clock Cycles, (6 ACQPS plus 1)
    ADC_setSocSampleWindow(myAdc, ADC_SocNumber_2, ADC_SocSampleWindow_7_cycles);   //set SOC2 S/H Window to 7 ADC Clock Cycles, (6 ACQPS plus 1)

    // Enable PWM clock
    CLK_enablePwmClock(myClk, PWM_Number_1);
    
    // Setup PWM
    PWM_enableSocAPulse(myPwm);                                         // Enable SOC on A group
    PWM_setSocAPulseSrc(myPwm, PWM_SocPulseSrc_CounterEqualCmpAIncr);   // Select SOC from from CPMA on upcount
    PWM_setSocAPeriod(myPwm, PWM_SocPeriod_FirstEvent);                 // Generate pulse on 1st event
    PWM_setCmpA(myPwm, 0x0080);                                         // Set compare A value
    PWM_setPeriod(myPwm, 0x00FF);                                       // Set period for ePWM1
    PWM_setCounterMode(myPwm, PWM_CounterMode_Up);                      // count up and start

    // Wait for ADC interrupt
    for(;;)
    {
    }

}


interrupt void adc_isr(void)
{
 
    //Save ADCRESULT1 and ADCRESULT2 in Respective Signal Variables
	Sig1_Voltage = ADC_readResult(myAdc, ADC_ResultNumber_1);
	Sig2_Voltage = ADC_readResult(myAdc, ADC_ResultNumber_2);

	//Update State of GPIOS Based on ADC conversion results
	if(Sig1_Voltage > high1)
	{
		GPIO_setHigh(myGpio, GPIO_Number_28);
		GPIO_setLow(myGpio, GPIO_Number_29);
	}
	else if (Sig1_Voltage > mid1)
	{
		GPIO_setHigh(myGpio, GPIO_Number_29);
		GPIO_setLow(myGpio, GPIO_Number_28);
	}
	else
	{
		GPIO_setHigh(myGpio, GPIO_Number_28);
		GPIO_setHigh(myGpio, GPIO_Number_29);
	}

	if(Sig2_Voltage > high2)
	{
		GPIO_setHigh(myGpio, GPIO_Number_34);
		GPIO_setLow(myGpio, GPIO_Number_18);
	}
	else if (Sig2_Voltage > mid2)
	{
		GPIO_setHigh(myGpio, GPIO_Number_18);
		GPIO_setLow(myGpio, GPIO_Number_34);
	}
	else
	{
		GPIO_setHigh(myGpio, GPIO_Number_34);
		GPIO_setHigh(myGpio, GPIO_Number_18);
	}


    // Clear ADCINT1 flag reinitialize for next SOC
    ADC_clearIntFlag(myAdc, ADC_IntNumber_1);
    // Acknowledge interrupt to PIE
    PIE_clearInt(myPie, PIE_GroupNumber_10);

    return;
}


