# TP 1



## Simulaciones

### Paquete generador de funciones

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



## Author

Marcos Dominguez
[@mrds90](https://github.com/mrds90)
