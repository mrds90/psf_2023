
/*=============================================================================
 * Author: Marcos Dominguez <mrds0690@gmail.com>
 * Date: 2021/08/10
 *===========================================================================*/

/*=====[Inclusions of function dependencies]=================================*/
#include "sense.h"
#include "board.h"

/*=====[Definition macros of private constants]==============================*/

#if (USED_ADC == 0)
#define LPC_ADC LPC_ADC0
#elif (USED_ADC == 1)
#define LPC_ADC LPC_ADC1
#elif (USED_ADC == 2)
#define LPC_ADC LPC_ADCHS
#endif


#define USED_CH  ADC_CH1
/*=====[Definitions of extern global variables]==============================*/

/*=====[Definitions of public global variables]==============================*/

/*=====[Definitions of private global variables]=============================*/
static uint16_t data;
static bool data_available;
static const LPC43XX_IRQn_Type adc_irq_map[3] = {ADC0_IRQn, ADC1_IRQn, ADCHS_IRQn};
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

    Chip_ADC_Init(LPC_ADC, &ADCSetup);

    Chip_ADC_SetBurstCmd(LPC_ADC, DISABLE);

    Chip_ADC_SetResolution(LPC_ADC, &ADCSetup, ADC_10BITS);

    Chip_ADC_SetSampleRate(LPC_ADC, &ADCSetup, ADC_MAX_SAMPLE_RATE / SAMPLE_RATE_FACTOR);
    /* Disable all channels */
    for (ADC_CHANNEL_T ch = ADC_CH0; ch <= ADC_CH7; ch++) {
        Chip_ADC_EnableChannel(LPC_ADC, ch, DISABLE);
        Chip_ADC_Int_SetChannelCmd(LPC_ADC, ch, DISABLE);
    }
    /* Enable used channel */
    Chip_ADC_EnableChannel(LPC_ADC, USED_CH, ENABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC, USED_CH, ENABLE);

    NVIC_EnableIRQ(adc_irq_map[USED_ADC]);
}

void ADC0_IRQHandler(void) {
    if (ADCCallback != NULL) {
        ADCCallback(ADC_context);
    }
}

void ADCDisable(void) {
    Chip_ADC_EnableChannel(LPC_ADC, USED_CH, DISABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC, USED_CH, DISABLE);
}

void ADCEnable(void) {
    Chip_ADC_EnableChannel(LPC_ADC, USED_CH, ENABLE);
    Chip_ADC_Int_SetChannelCmd(LPC_ADC, USED_CH, ENABLE);
}

void ADCRead(void) {
    Chip_ADC_ReadValue(LPC_ADC, USED_CH, &data);
    data_available = true;
}

void ADCStartConversion(void) {
    Chip_ADC_SetStartMode(LPC_ADC, ADC_START_NOW, ADC_TRIGGERMODE_FALLING);
}

bool ADCDataAvailable(void) {
    return data_available;
}

uint16_t ADCDataValue(void) {
    data_available = false;
    return data;
}
