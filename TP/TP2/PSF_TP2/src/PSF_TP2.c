/*=============================================================================
 * Author: Marcos Dominguez <mrds0690@gmail.com>
 * Date: 2023/09/10
 * Version: 1
 *===========================================================================*/

/*=====[Inclusions of function dependencies]=================================*/

#include "PSF_TP2.h"
#include "sapi.h"
#include "arm_math.h" // Incluir la librería CMSIS
#include "string.h"
#include "sense.h"
#include "sapi_uart.h"
#include "cmsis_gcc.h"
#include "timer_config.h"
/*=====[Definition macros of private constants]==============================*/

#define RESOLUTION(data, bit)  (data >> (10 - bit))

#define SAMPLE_RATE (ADC_MAX_SAMPLE_RATE / 64)
/*=====[Definition of private methods]=======================================*/

/*=====[Definitions of extern global variables]==============================*/

/*=====[Definitions of public global variables]==============================*/

/*=====[Definitions of private global variables]=============================*/

/*=====[Main function, program entry point after power on or reset]==========*/


static void FSMMainPrgInit(void);

static void ISRAdquisition(void *not_used);

static void ISRSampleBaseTime(void *not_used);

static void ISRUartTx(void *not_used);

static bool_t data_sent = TRUE;

static uint32_t frec = 0;

static uint32_t count = 0;

int main(void) {
    // ----- Setup -----------------------------------
    FSMMainPrgInit();
    // ----- Repeat for ever -------------------------
    while (TRUE) {
        __WFI();
    }
    return 0;
}

static void FSMMainPrgInit(void) {
    boardConfig();
    uartConfig(UART_USB, 460800);
    cyclesCounterInit(EDU_CIAA_NXP_CLOCK_SPEED);
    uartInterrupt(UART_USB, TRUE);
    uartCallbackSet(UART_USB, UART_TRANSMITER_FREE, ISRUartTx, NULL);
    TIMER_CONFIG_Init(SAMPLE_RATE, ISRSampleBaseTime);
    ADCConfig(ISRAdquisition, NULL);
}

/*=====[Implementation of private interrupt functions]=================*/
#define ADC_BIT_RESOLUTION 10
static int16_t adc_value = 0;
static void ISRAdquisition(void *not_used) {
    static uint32_t count = 0;
    count++;
    if (count == ((SAMPLE_RATE) / 2)) {
        count = 0;
        gpioToggle(LED2);
    }
    ADCRead();

    if (data_sent > 0) {
        adc_value = RESOLUTION((ADCDataValue() - 512), ADC_BIT_RESOLUTION);
        uartInterrupt(UART_USB, true);
            #if (ADC_BIT_RESOLUTION < 9)
        uartTxWrite(UART_USB, (int8_t)(adc_value));
            #else
        uartTxWrite(UART_USB, (int8_t)(adc_value >> 8));
            #endif
        data_sent = FALSE;
    }
    ADCDisable();
}

static void ISRUartTx(void *not_used) {
    static uint32_t count = 0;
    count++;
    if (count == ((SAMPLE_RATE) / 2)) {
        count = 0;
        gpioToggle(LED3);
    }

    #if (ADC_BIT_RESOLUTION < 9)
    data_sent = TRUE;
    uartInterrupt(UART_USB, false);
    #else
    if (data_sent == FALSE) {
        uartTxWrite(UART_USB, (int8_t)(adc_value));
        data_sent = TRUE;
        uartInterrupt(UART_USB, false);
    }
    #endif
}

static void ISRSampleBaseTime(void *not_used) {
    static uint32_t count = 0;
    count++;
    if (count == ((SAMPLE_RATE) / 2)) {
        count = 0;
        gpioToggle(LED1);
    }
    ADCEnable();
}
