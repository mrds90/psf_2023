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

#define SAMPLE_RATE (ADC_MAX_SAMPLE_RATE / SAMPLE_RATE_FACTOR)

#define SYNC_HEAD   0xA5

#define ADC_BIT_RESOLUTION 10

typedef enum {
    SEND_STATE_HEAD,
    SEND_STATE_HIGH,
    SEND_STATE_LOW,
} send_state_t;
/*=====[Definition of private methods]=======================================*/

/*=====[Definitions of extern global variables]==============================*/

/*=====[Definitions of public global variables]==============================*/

/*=====[Definitions of private global variables]=============================*/

/*=====[Main function, program entry point after power on or reset]==========*/


static void FSMMainPrgInit(void);

static void ISRAdquisition(void *not_used);

static void ISRSampleBaseTime(void *not_used);

static void ISRUartTx(void *not_used);

static send_state_t data_sent = SEND_STATE_HEAD;

static uint32_t frec = 0;

int main(void) {
    // ----- Setup -----------------------------------
    FSMMainPrgInit();
    // ----- Repeat for ever -------------------------
    while (true) {
        __WFI();
    }
    return 0;
}

static void FSMMainPrgInit(void) {
    boardConfig();
    uartConfig(UART_USB, 460800);
    cyclesCounterInit(EDU_CIAA_NXP_CLOCK_SPEED);
    uartInterrupt(UART_USB, true);
    uartCallbackSet(UART_USB, UART_TRANSMITER_FREE, ISRUartTx, NULL);
    TIMER_CONFIG_Init(SAMPLE_RATE, ISRSampleBaseTime);
    ADCConfig(ISRAdquisition, NULL);
}

/*=====[Implementation of private interrupt functions]=================*/

static int16_t adc_value = 0;
static void ISRAdquisition(void *not_used) {
    static uint32_t count = 0;
    count++;
    if (count == ((SAMPLE_RATE) / 2)) {
        count = 0;
        gpioToggle(LED2);
    }
    ADCRead();

    if (data_sent == SEND_STATE_HEAD) {
        adc_value = RESOLUTION((ADCDataValue() - 512), ADC_BIT_RESOLUTION);
        uartInterrupt(UART_USB, true);
        uartTxWrite(UART_USB, SYNC_HEAD);
        data_sent = SEND_STATE_HIGH;
    }
}

static void ISRUartTx(void *not_used) {
    static uint32_t count = 0;
    count++;
    if (count == ((SAMPLE_RATE) / 2)) {
        count = 0;
        gpioToggle(LED3);
    }

    if (data_sent == SEND_STATE_HIGH) {
        data_sent = SEND_STATE_LOW;
        uartTxWrite(UART_USB, (int8_t)(adc_value >> 8));
    }
    else if (data_sent == SEND_STATE_LOW) {
        data_sent = SEND_STATE_HEAD;
        uartTxWrite(UART_USB, (int8_t)(adc_value));
        uartInterrupt(UART_USB, false);
    }
}

static void ISRSampleBaseTime(void *not_used) {
    static uint32_t count = 0;
    count++;
    if (count == ((SAMPLE_RATE) / 2)) {
        count = 0;
        gpioToggle(LED1);
    }
    ADCStartConversion();
}
