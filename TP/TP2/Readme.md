# TP 2

## DFT

### Funciones típicas y su espectro

En el siguiente script puede encontrar como se genera la información de esta sección: [DFTOfTipicalFunction.py](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP2/DFTOfTipicalFunction.py)

Se generó un script que simula señales de típicas de 10Hz y amplitud 1 con una frecuencia de muestreo de 1000Hz y 1000 muestras.
A continuación se detalla la información de la señales generadas:
- Señal Senoidal:
    - A) Frecuencia: 10 Hz
    - B) Amplitud: 1.0
    - C) Potencia promedio: 0.5
    - D) Frecuencia de muestreo: 1000 Hz
    - E) Numero de muestras: 1000

- Señal Cuadrada:
    - A) Frecuencia: 10 Hz
    - B) Amplitud: 1.0
    - C) Potencia promedio: 0.999
    - D) Frecuencia de muestreo: 1000 Hz
    - E) Numero de muestras: 1000

- Señal Triangular:
    - A) Frecuencia: 10 Hz
    - B) Amplitud: 1.0
    - C) Potencia promedio: 0.3336
    - D) Frecuencia de muestreo: 1000 Hz
    - E) Numero de muestras: 1000

- Señal Delta en t=0:
    - B) Amplitud: 1.0
    - C) Potencia promedio: 0.001
    - D) Frecuencia de muestreo: 1000 Hz
    - E) Numero de muestras: 1000

A continuación se puede observar las señales con su espectro asociado:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TP2/figures/TipicalSingalsPlusDFT.png)

### Resolución espectral

Se cargo el archivo txt y se graficó el espectro de la señal en el siguiente script de python: [SpectralResolution.py](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP2/SpectralResolution.py)

Como se observa en la siguiente figura, la frecuencia predominante en esta señal aparenta ser 50Hz:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TP2/figures/ZeroPaddingRaw.png)

Se aplica la estrategia de zero padding, que consiste en agregar ceros a la señal para mejorar la resolución espectral (dada por fs/n_samples), y se obtiene lo siguiente:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TP2/figures/ZeroPaddingProcess.png)

En esta nueva gráfica se puede observar que había 2 frecuencias predominantes (en 50 y 52.6 Hz) y varios componentes frecuenciales de menor magnitud en el resto del espectro observable para esa frecuencia de muestro.

Todas las gráficas pueden fueron extraídas con el script mencionado al inicio de esta sección.

### Imagen 2D 

Se levanto del archivo fft_hjs.npy el espectro de la señal y se trataba de un espectro complejo cuya señal también tenía elementos complejos.

Se graficó la señal como un mapeo 2-D en el plano complejo y se obtuvo la siguiente figura:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TP2/figures/SignalHJS.png)

Se genero un script que permite recortar el espectro de forma tal de comprimir el mismo. Observando el espectro original se puede observar
que por encima de 200 (no tiene unidad conocida) la energía de la señal es muy baja. Por lo que se prueba recortar este y volver a evaluar la señal.

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TP2/figures/SignalHJSSpectrumToCut.png)

El nuevo espectro es el siguiente:

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TP2/figures/SignalHJSSpectrumCutted.png)

y la señal se observa de la siguiente manera

![alt text](https://raw.githubusercontent.com/mrds90/psf_2023/MSE_Dominguez/TP/TP2/figures/SignalHJSFiltered.png)

Todas las gráficas pueden fueron extraídas con el script [UnknownSignalSpectrum](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP2/UnknownSignalSpectrum.py)








## Author

Marcos Dominguez
[@mrds90](https://github.com/mrds90)
