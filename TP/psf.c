#include "arm_math.h"
#include "sapi.h"
#include "string.h"
#include "stdio.h"
#include "fir.h"

#define SCT_PWM_PIN_LED 2
#define SCT_PWM_LED 2
#define SCT_ADC_PIN_OUT 8
#define SCT_ADC_OUT 1
#define ADC_FRAME_SAMPLES 20000
#define ADC_TIGGER_VALUE 0
#define ADC_SAMPLE_RATE 8000
#define ADC_BITS 10
#define ADC_MUTE_WAIT 64
#define ADC_MUTE_GAP_BITS 4 
#define ADC_MUTE_LOW  -256
#define ADC_MUTE_HIGH 256
#define FI_TOLERANCE 15

    char pre[8];
    uint32_t id;
    uint16_t N;
    uint16_t fs;
    uint16_t fi[4];
    char key;
    char pos[4];
} __attribute__((packed)) header = {
    "*header*", 0, ADC_FRAME_SAMPLES, ADC_SAMPLE_RATE, {0, 0, 0, 0,}, '?', "end*"};

int16_t adc[ADC_FRAME_SAMPLES] __attribute__((section (".data.$RamLoc40")));
// int16_t adc[ADC_FRAME_SAMPLES] __attribute__((section (".data.$RamLoc40")));
// int16_t * adc = (int16_t *)(0x20000000);

int16_t fft[1] __attribute__((section (".data.$RamAHB32")));
// int16_t buffer[2 * ADC_FRAME_SAMPLES];
char cadena[64];
volatile uint16_t index;
// arm_rfft_instance_q15 descriptor;

void ADC0_IRQHandler(void) {
    static enum {
        ESPERANDO_MENOR,
        ESPERANDO_MAYOR,
        MUESTREANDO,
        ESPERANDO_SILENCIO,
    } estado = ESPERANDO_MENOR;
    static u_int16_t waiting;
    uint16_t sample;
    int16_t value;

    Chip_ADC_ReadValue(LPC_ADC0, ADC_CH1, &sample);
    value = (((sample - 512)) >> (10 - ADC_BITS)) << (6 + (10 - ADC_BITS));

    if (index == 0) {
        switch (estado) {
            case MUESTREANDO:
                waiting = 0;
                estado = ESPERANDO_SILENCIO;
                gpioWrite(LED1, false);
                gpioWrite(LED2, true);
                break;
            case ESPERANDO_MENOR:
                if (value < ADC_TIGGER_VALUE) estado = ESPERANDO_MAYOR;
                break;
            case ESPERANDO_MAYOR:
                gpioWrite(LED1, true);
                if (value > ADC_TIGGER_VALUE) {
                    estado = MUESTREANDO;
                    gpioWrite(LED1, true);
                }
                break;
            case ESPERANDO_SILENCIO:
                if ((value < ADC_MUTE_LOW) || (value > ADC_MUTE_HIGH)) {
                    waiting = 0;
                } else {
                    waiting++;
                    if (waiting==ADC_MUTE_WAIT) {
                        estado = ESPERANDO_MENOR;
                        gpioWrite(LED1, false);
                        gpioWrite(LED2, false);
                    }
                }
            default:
                break;
        }
    }
    if (estado == MUESTREANDO) {
        adc[index] = value;
        index++;        
    }
}

void adc_init(void) {
    ADC_CLOCK_SETUP_T adc;

    Chip_ADC_Init(LPC_ADC0, &adc);
    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH1, ENABLE);

    Chip_ADC_SetStartMode(LPC_ADC0, ADC_START_ON_CTOUT8, ADC_TRIGGERMODE_FALLING);
    NVIC_EnableIRQ(ADC0_IRQn);
}

void sct_init(void) {
    uint16_t dutty = Chip_SCTPWM_GetTicksPerCycle(LPC_SCT) / 2;

    Chip_SCTPWM_Init(LPC_SCT);
    Chip_SCTPWM_SetRate(LPC_SCT, ADC_SAMPLE_RATE);

    Chip_SCTPWM_SetOutPin(LPC_SCT, SCT_ADC_OUT, SCT_ADC_PIN_OUT);
    Chip_SCTPWM_SetDutyCycle(LPC_SCT, SCT_ADC_OUT, dutty);

    Chip_SCTPWM_Start(LPC_SCT);
}

int main(void) {
    boardConfig();
    uartConfig(UART_USB, 460800);

    adc_init();
    sct_init();

    while (1) {
        index = 0;
        Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, ENABLE);
        while (index < header.N) {
            __WFI();
        };
        Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, DISABLE);

        gpioToggle(LED3);
        arm_conv_fast_q15(adc, header.N, h, h_LENGTH, fft); //se podria reutilizar el adc en vez de y como salida
        // memcpy(fft, adc, sizeof(fft));
        // arm_rfft_init_q15(&descriptor, ADC_FRAME_SAMPLES, 0, 1);
        // arm_rfft_q15(&descriptor, fft, buffer);
        // arm_cmplx_mag_squared_q15(buffer, fft, ADC_FRAME_SAMPLES);
        // header.N += h_LENGTH - 1;
        header.id++;
        uartWriteByteArray(UART_USB, (uint8_t *)&header, sizeof(header));
        uartWriteByteArray(UART_USB, (uint8_t *)adc, 2 * header.N);
        uartWriteByteArray(UART_USB, (uint8_t *)fft, 2 * header.N);
    }
}
