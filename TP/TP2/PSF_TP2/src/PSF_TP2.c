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
#include "fir_band_pass_ecg_5-20hz.h"
/*=====[Definition macros of private constants]==============================*/

#define RESOLUTION(data, bit)  ((data) >> (10 - (bit)))

#define SAMPLE_RATE (ADC_MAX_SAMPLE_RATE / SAMPLE_RATE_FACTOR)

#define SYNC_HEAD   0xA5

#define ADC_BIT_RESOLUTION 10

#define THRESHOLD   40

#define SEG_MIN_REL     (60)

#define PPM_FROM_COUNT(d_cuentas) (SAMPLE_RATE * SEG_MIN_REL / (d_cuentas))
#define COUNT_FROM_PPM(ppm) (SAMPLE_RATE * SEG_MIN_REL / (ppm))
typedef enum {
    SEND_STATE_HEAD,
    SEND_STATE_HIGH,
    SEND_STATE_LOW,
} send_state_t;
/*=====[Definition of private methods]=======================================*/

/*=====[Definitions of extern global variables]==============================*/

/*=====[Definitions of public global variables]==============================*/
static uint8_t ppm = 120;
/*=====[Definitions of private global variables]=============================*/

/*=====[Main function, program entry point after power on or reset]==========*/


static void FSMMainPrgInit(void);

static void ISRAdquisition(void *not_used);

static void ISRSampleBaseTime(void *not_used);

static void ISRUartTx(void *not_used);

static send_state_t data_sent = SEND_STATE_HEAD;

static uint32_t frec = 0;

static uint32_t count = 0;

int main(void) {
    // ----- Setup -----------------------------------
    FSMMainPrgInit();
    // ----- Repeat for ever -------------------------
    while (true) {
        __WFI();

        if ((count % SAMPLE_RATE) == 0) {
            printf("%d\n ", ppm);
            gpioToggle(LED3);
        }
    }
    return 0;
}

static void FSMMainPrgInit(void) {
    // boardConfig();
    uartConfig(UART_USB, 460800);
    cyclesCounterInit(EDU_CIAA_NXP_CLOCK_SPEED);
    // uartInterrupt(UART_USB, true);
    // uartCallbackSet(UART_USB, UART_TRANSMITER_FREE, ISRUartTx, NULL);
    TIMER_CONFIG_Init(SAMPLE_RATE, ISRSampleBaseTime);
    ADCConfig(ISRAdquisition, NULL);
}

/*=====[Implementation of private interrupt functions]=================*/
#define MA_BITS  (6)
#define MA_SIZE  (1 << MA_BITS)
static uint32_t offset_ac = 0;
static uint16_t offset_buffer[MA_SIZE] = {[0 ... (MA_SIZE - 1)] = 0};
static uint16_t ma_index = 0;
static uint16_t offset = 0;
static int16_t adc_data[MA_SIZE] = {[0 ... (MA_SIZE - 1)] = 0};
static int16_t filtered_data[h_PADD_LENGTH + MA_SIZE - 1] = {[0 ... (h_PADD_LENGTH - 1)] = 0};
static int16_t filtered_data3[h_PADD_LENGTH + MA_SIZE - 1] = {[0 ... (h_PADD_LENGTH - 1)] = 0};

static uint32_t last_max_count = 0;

static int16_t silenced_count = 0;
static void ISRAdquisition(void *not_used) {
    ADCRead();
    count++;
    silenced_count--;
    if (silenced_count < 0) {
        silenced_count = 0;
    }

    offset_ac -= offset_buffer[ma_index];
    offset_buffer[ma_index] = ADCDataValue();
    offset_ac += offset_buffer[ma_index];
    offset = (offset_ac >> MA_BITS);
    ma_index = (ma_index + 1) & (MA_SIZE - 1);     //mask of 9 bits
    memmove(adc_data, &adc_data[1], sizeof(int16_t) * (MA_SIZE - 1));
    adc_data[MA_SIZE - 1] = RESOLUTION((offset_buffer[ma_index] - offset), ADC_BIT_RESOLUTION);
    arm_conv_fast_q15(adc_data, MA_SIZE, h, h_LENGTH, filtered_data);
    arm_mult_q15(filtered_data, filtered_data, filtered_data3, h_PADD_LENGTH + MA_SIZE - 1);
    arm_mult_q15(filtered_data, filtered_data3, filtered_data3, h_PADD_LENGTH + MA_SIZE - 1);

    if (silenced_count == 0) {
        if ((filtered_data[(h_LENGTH / 2)] - THRESHOLD)  > 0) {
            ppm = PPM_FROM_COUNT(count - last_max_count);
            last_max_count = count;
            silenced_count = COUNT_FROM_PPM(100);
            gpioToggle(LED2);
        }
    }


    // if (data_sent == SEND_STATE_HEAD) {
    //     uartInterrupt(UART_USB, true);
    //     uartTxWrite(UART_USB, SYNC_HEAD);
    //     data_sent = SEND_STATE_HIGH;
    // }
}

// static void ISRUartTx(void *not_used) {
//     static uint32_t count2 = 0;
//     count2++;
//     if (count2 == ((SAMPLE_RATE) / 2)) {
//         count2 = 0;
//         gpioToggle(LED3);
//     }

//     static int16_t freeze_data;
//     if (data_sent == SEND_STATE_HIGH) {
// //        freeze_data = 6 * (filtered_data[h_LENGTH / 2]);
// //        freeze_data = 6 * (filtered_data[h_LENGTH / 2] - THRESHOLD);
//         freeze_data = ppm;
//         // freeze_data = adc_data[MA_SIZE - 1];

//         data_sent = SEND_STATE_LOW;
//         uartTxWrite(UART_USB, (int8_t)(freeze_data >> 8));
//     }
//     else if (data_sent == SEND_STATE_LOW) {
//         data_sent = SEND_STATE_HEAD;
//         uartTxWrite(UART_USB, (int8_t)(freeze_data));
//         uartInterrupt(UART_USB, false);
//     }
// }

static void ISRSampleBaseTime(void *not_used) {
    static uint32_t count3 = 0;
    count3++;
    if (count3 == ((SAMPLE_RATE) / 2)) {
        count3 = 0;
        gpioToggle(LED1);
    }
    ADCStartConversion();
}
