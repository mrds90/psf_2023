# TP FINAL - Pulsaciones por minuto con EDU_CIAA

Sistema que cuenta pulsaciones por minuto en tiempo real.

## ECG
### Señal de interés
La señal de interés es la señal eléctrica del sistema cardíaco que tiene las siguientes morfología:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TPFinal/figures/ECGinTime.jpg)

Si analizamos frecuecialmente una adquisición de ECG no solo se observa la señal de interés, sino que aparecen ruidos provenientes de otros
artefactos involucrados en la adquisición. En la siguiente imagen se puede observar el espectro de la señal de ECG:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TPFinal/figures/ECGInFreq.png)

Para reducir la complejidad del problema se utilizó un front-end que acondiciona la señal y garantiza la ausencia de alias el la adquisición.
Ademas se adquirió a 2Khz que se encuentra bastante por encima del espectro de la señal a evaluar.

## Diseño del algoritmo

El algoritmo cuenta de 5 etapas que permites encontrar la onda R de un ECG para luego calcular el período de repetición de esta. Estos pasos son:
- Minimizar el offset.
- Reducir las componentes frecuenciales que no son de interés y quedarnos con el complejo QRS (10-14 Hz).
- Hacer la potencia cubica de la señal para resaltar los picos y mejorar la sensibilidad.
- Utilizar un threshold para definir el valor de pico.
- Definir un periodo de silencio (refractario) para evitar falsos positivos.

A la señal original se le aplica un filtro de ventana móvil para calcular el offset y se lo resta al valor de cada elemento adquirido por el ADC. Se puede observar el resultado en la siguiente figura:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TPFinal/figures/ECGMeasureRaw.png)

Con pyfda se diseño un filtro pasa banda para conservar la zona de interés. Se observa en la siguiente figura el filtro diseñado:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TPFinal/figures/FilterPYFDA.png)

Este filtro se aplica utilizando la convolución rápida en el tiempo y luego se aplica la 3ra potencia y el resultado se puede observar en la siguiente imagen:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TPFinal/figures/ECGMeasureFiltered.png)

Finalmente se resta un threshold para conservar solo los picos. En la siguiente figura se muestra la señal resultante con los valores negativos forzados a 0 para una mejore visualización:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TPFinal/figures/ECGMeasurePeaks.png)

Con este resultado solo basta con identificar cuando la señal empieza a ser mayor a 0 para tener el periodo de la señal con mucha precisión. Y a partir de ahi calcular la frecuencia cardíaca en Pulsaciones por Minuto (PPM).

Se muestra a continuación como el sistema reporta pulsaciones mediante un puerto serie:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TPFinal/figures/ECGMeasureFreq.png)


## Author

Marcos Dominguez
[@mrds90](https://github.com/mrds90)
