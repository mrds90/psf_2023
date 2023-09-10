/*=============================================================================
 * Author: Marcos Dominguez <mrds0690@gmail.com>
 * Date: 2023/09/10
 * Version: 1
 *===========================================================================*/

/*=====[Inclusions of function dependencies]=================================*/

#include "PSF_TP1.h"
#include "sapi.h"
#include "arm_math.h" // Incluir la librería CMSIS
#include "string.h"
/*=====[Definition macros of private constants]==============================*/
/*=====[Definition of private methods]=======================================*/

static uint16_t printQ7(q7_t n,char *buf);

/*=====[Definitions of extern global variables]==============================*/

/*=====[Definitions of public global variables]==============================*/

/*=====[Definitions of private global variables]=============================*/

/*=====[Main function, program entry point after power on or reset]==========*/

int main( void )
{
   // ----- Setup -----------------------------------
   boardInit();

   // ----- Repeat for ever -------------------------
   static q7_t q7_num1, q7_num2, q7_result;
   static delay_t delay;
   delayConfig(&delay, 2000);
   while( true ) {
      if(delayRead(&delay)) {
         // Asignar valores Q7
         q7_num1 = 0x40;
         q7_num2 = 0x23;
         q7_t res = (((q7_num1 * q7_num2)<<1) >>8);
         // Realizar una multiplicación
         arm_mult_q7(&q7_num1, &q7_num2, &q7_result,1);
         char str[50];
         printf("by dsp: ");
         printQ7(q7_result,str);
         printf(str);
         printf("by soft: ");
         printQ7(res,str);
         printf(str);
         gpioToggle(LED1);
      }
   }


   return 0;
}


static uint16_t printQ7(q7_t n,char *buf)
{
   int i;
   float ans=(n&0x80)?-1:0;
   for(i=1;i<8;i++)
   {
      if(n&(0x80>>i)){
         ans+=1.0/(1U<<i);
      }
   }
   return sprintf(buf,"q7: 0x%X - float:%.8f\r\n",n,ans);
}