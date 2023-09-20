import numpy as np
import matplotlib.pyplot as plt
from FuncGenerator import *

fs = 1000  # Frecuencia de muestreo
f0 = 10    # Frecuencia de las señales
amp = 1.0  # Amplitud de las señales
samples = 1000  # Número de muestras

# Generar las señales
t_sin, sin_values = SinFunc(fs, f0, amp, samples)
t_square, square_values = SquareFunc(fs, f0, amp, samples)
t_triangular, triangular_values = TriangularFunc(fs, f0, amp, samples)
t_delta, delta_values = DeltaFunc(fs, samples)

# Calcular el espectro de frecuencia
frequencies = np.fft.fftfreq(samples, 1 / fs)
spectrum_sin = np.fft.fft(sin_values)
spectrum_square = np.fft.fft(square_values)
spectrum_triangular = np.fft.fft(triangular_values)
spectrum_delta = np.fft.fft(delta_values)

# Graficar las señales y sus espectros
plt.figure(figsize=(12, 8))

print("Señal Senoidal:")
print("A) Frecuencia:", f0, "Hz")
print("B) Amplitud:", amp)
print("C) Potencia promedio:", np.mean(sin_values**2))
print("D) Frecuencia de muestreo:", fs, "Hz")
print("E) Numero de muestras:", samples)
print()

plt.subplot(2, 4, 1)
plt.plot(t_sin, sin_values)
plt.title("Senoidal")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

print("Señal Cuadrada:")
print("A) Frecuencia:", f0, "Hz")
print("B) Amplitud:", amp)
print("C) Potencia promedio:", np.mean(square_values**2))
print("D) Frecuencia de muestreo:", fs, "Hz")
print("E) Numero de muestras:", samples)
print()
plt.subplot(2, 4, 2)
plt.plot(t_square, square_values)
plt.title("Cuadrada")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

print("Señal Triangular:")
print("A) Frecuencia:", f0, "Hz")
print("B) Amplitud:", amp)
print("C) Potencia promedio:", np.mean(triangular_values**2))
print("D) Frecuencia de muestreo:", fs, "Hz")
print("E) Numero de muestras:", samples)
print()

plt.subplot(2, 4, 3)
plt.plot(t_triangular, triangular_values)
plt.title("Triangular")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

print("Señal Delta en t=0:")
print("A) Frecuencia:", f0, "Hz")
print("B) Amplitud:", amp)
print("C) Potencia promedio:", np.mean(delta_values**2))
print("D) Frecuencia de muestreo:", fs, "Hz")
print("E) Numero de muestras:", samples)
print()
plt.subplot(2, 4, 4)
plt.plot(t_delta, delta_values)
plt.title("Delta en t=0")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

plt.subplot(2, 4, 5)
plt.plot(frequencies, np.abs(spectrum_sin))
plt.title("Espectro Senoidal")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

plt.subplot(2, 4, 6)
plt.plot(frequencies, np.abs(spectrum_square))
plt.title("Espectro Cuadrada")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

plt.subplot(2, 4, 7)
plt.plot(frequencies, np.abs(spectrum_triangular))
plt.title("Espectro Triangular")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

plt.subplot(2, 4, 8)
plt.plot(frequencies, np.abs(spectrum_delta))
plt.title("Espectro Delta en t=0")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

plt.tight_layout()
plt.show()
