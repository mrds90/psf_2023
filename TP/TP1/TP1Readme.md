# TP 1



## 3 - Simulaciones

### 3.1 - Paquete generador de funciones

Se genero un paquete generador de funciones en el módulo FuncGenerator.py:
```
import numpy as np


def SinFunc(fs: float, f0: float, amp: float = 1.0, samples: int = 100, phase: float = 0.0):
    t = np.arange(0, samples) / fs
    sin = (amp * np.sin(2 * np.pi * f0 * t + 2 * np.pi * phase))
    return t, sin


def SquareFunc(fs: float, f0: float, amp: float = 1.0, samples: int = 100):
    t = np.arange(0, samples) / fs
    square = (amp * np.sign(np.sin(2 * np.pi * f0 * t)))
    return t, square


def TriangularFunc(fs: float, f0: float, amp: float, samples: int):
    t = np.arange(0, samples) / fs
    triangular_wave = (2 * amp / np.pi) * np.arcsin(np.sin(2 * np.pi * f0 * t))
    return t, triangular_wave

```

Se probó en el Script TP1FuncGeneratorExample.py

```
fs = 1000  # Frecuencia de muestreo en Hz
f0 = 1    # Frecuencia de la señal en Hz
amp = 0.8  # Amplitud de la señal
samples = 2000  # Número de muestras
phase = 0.5
# Generar la señal sinusoidal
t_sin, sinusoidal_signal = SinFunc(fs, f0, amp, samples,phase)
t_square, square_signal = SquareFunc(fs, f0, amp, samples)
t_triangular, triangular_signal = TriangularFunc(fs, f0, amp, samples)

```
y se graficó utilizando la biblioteca plot de matplotlib

![alt text](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP1/figures/FuncGenFs1000F01Amp0_8Phase0_5.png?raw=true)

![alt text](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP1/figures/FuncGenFs1000F02Amp0_4Phase0_25.png?raw=true)

![alt text](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP1/figures/FuncGenFs3000F04Amp1_0Phase0_75.png?raw=true)

### 3.2 - Simulación con Alias

Se generó la simulación propuesta en el ejercicio.

```
from FuncGenerator import *
from matplotlib import pyplot as plt

fs = 1000  # Frecuencia de muestreo en Hz
amp = 1.0  # Amplitud de la señal
samples = 1000  # Número de muestras
phase = 0.0
# Generar la señal sinusoidal
t_sin1_1, sinusoidal_signal0 = SinFunc(fs, 1.1 *fs, amp, samples,phase)
t_sin0_1, sinusoidal_signal1 = SinFunc(fs, 0.1 *fs, amp, samples,phase)

t_sin0_49, sinusoidal_signal2 = SinFunc(fs, 0.49 *fs, amp, samples,phase)
t_sin0_51, sinusoidal_signal3 = SinFunc(fs, 0.51 *fs, amp, samples,phase)
t_sin0_49C, sinusoidal_signal4 = SinFunc(fs*10, 0.49 *fs, amp, samples,phase)
```

En el primer caso se observa un claro ejemplo en donde la frecuencia de la señal es muy superior a la frecuencia de muestreo / 2 
y la misma se observa en el espectro como una señal de 0.1 * fs. 
Este fenómeno, teóricamente conocido como aliasing, se refiere a la aparición de una señal en el rango entre -fs/2 y fs/2 en el espectro cuya frecuencia natural esta fuera de este rango. Para determinar la frecuencia a la que esta señal aparecerá dentro de ese rango, se realizan restas sucesivas de la frecuencia de muestreo (fs) a la frecuencia original de la señal hasta que la frecuencia resultante esté dentro del espectro observable definido por la frecuencia de muestreo (fs).

En el segundo caso se observa una situación similar, solo que al restar la frecuencia de muestreo a la señal que de 0.51 * fs la misma queda 
en el lado negativo del espectro, es decir con la fase invertida.
![alt text](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP1/figures/TP1-3_2_2Alias.png?raw=true)


### 5.2 - Ruido de cuantización

Se realizo en la edu-ciaa el circuito propuesto que consistía en un capacitor de desacople, un filtro rc como anti alias y
un divisor resistivo para centrar en 1.65 el punto medio de la aquicisión. En la siguiente imagen se ve el circuito montado:

![alt text](https://github.com/mrds90/psf_2023/blob/MSE_Dominguez/TP/TP1/figures/TP1-5_2-SetUp.jpeg?raw=true)



## Author

Marcos Dominguez
[@mrds90](https://github.com/mrds90)
