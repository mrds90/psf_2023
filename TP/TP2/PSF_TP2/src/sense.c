
/*=============================================================================
 * Author: Marcos Dominguez <mrds0690@gmail.com>
 * Date: 2021/08/10
 *===========================================================================*/

/*=====[Inclusions of function dependencies]=================================*/
#include "sapi.h"
#include "sense.h"
#include "board.h"

/*=====[Definition macros of private constants]==============================*/

/*=====[Definitions of extern global variables]==============================*/

/*=====[Definitions of public global variables]==============================*/

/*=====[Definitions of private global variables]=============================*/
static uint16_t data;
static bool_t data_available;
/*=====[Function Implementations]============================================*/

void (*ADCCallback)(void *) = NULL;
void *ADC_context = 0;

/* P0.23 -> AD0 */
void ADCConfig(void *ptr_function, void *context) {
    ADCCallback = ptr_function;
    ADC_context = context;
    /* Config ADC0 sample mode */
    ADC_CLOCK_SETUP_T ADCSetup = {
        1,   // ADC Sample rate:ADC_MAX_SAMPLE_RATE = 400KHz
        10,                    // ADC resolution: ADC_10BITS = 10
        0                      // ADC Burst Mode: (true or false)
    };

    Chip_ADC_Init(LPC_ADC0, &ADCSetup);
    /* Enable  burst mode */
    Chip_ADC_SetBurstCmd(LPC_ADC0, ENABLE);

    Chip_ADC_SetResolution(LPC_ADC0, &ADCSetup, ADC_10BITS);

    Chip_ADC_SetSampleRate(LPC_ADC0, &ADCSetup, ADC_MAX_SAMPLE_RATE / 64);
    /* Disable all channels */
    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH1, DISABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, DISABLE);

    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH2, DISABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH2, DISABLE);

    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH3, DISABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH3, DISABLE);

    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH4, DISABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH4, DISABLE);

    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH1, ENABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, ENABLE);

    NVIC_EnableIRQ(ADC0_IRQn);
}

void ADC0_IRQHandler(void) {
    if (ADCCallback != NULL) {
        ADCCallback(ADC_context);
    }
}

void ADCDisable(void) {
    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH1, DISABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, DISABLE);
}

void ADCEnable(void) {
    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH1, ENABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, ENABLE);
}

void ADCRead(void) {
    Chip_ADC_ReadValue(LPC_ADC0, ADC_CH1, &data);
    data_available = TRUE;
}

bool_t ADCDataAvailable(void) {
    return data_available;
}

uint16_t ADCDataValue(void) {
    data_available = FALSE;
    return data;
}
