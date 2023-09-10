from FuncGenerator import *
from matplotlib import pyplot as plt

fs = 1000  # Frecuencia de muestreo en Hz
f0 = 1    # Frecuencia de la señal en Hz
amp = 0.8  # Amplitud de la señal
samples = 2000  # Número de muestras
phase = 0.5
# Generar la señal sinusoidal
t_sin, sinusoidal_signal = SinFunc(fs, f0, amp, samples,phase)
t_square, square_signal = SquareFunc(fs, f0, amp, samples)
t_triangular, triangular_signal = TriangularFunc(fs, f0, amp, samples)

# Crear un subplot con 3 gráficas
plt.figure(figsize=(12, 6))

# Gráfica 1: Señal Sinusoidal
plt.subplot(3, 1, 1)
plt.plot(t_sin, sinusoidal_signal, label='Señal Sinusoidal')
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.ylabel('Amplitud')
plt.title('Señales: Sinusoidal, Cuadrada y Triangular')
plt.legend()

# Gráfica 2: Señal Cuadrada
plt.subplot(3, 1, 2)
plt.plot(t_square, square_signal, label='Señal Cuadrada')
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.ylabel('Amplitud')
plt.legend()

# Gráfica 3: Señal Triangular
plt.subplot(3, 1, 3)
plt.plot(t_triangular, triangular_signal, label='Señal Triangular')
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()

plt.tight_layout()
plt.show()