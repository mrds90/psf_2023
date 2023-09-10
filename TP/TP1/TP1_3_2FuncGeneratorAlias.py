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

# Crear un subplot con 3 gráficas
plt.figure(figsize=(12, 6))
ax1 = plt.subplot(2, 1, 1)
plt.plot(t_sin1_1, sinusoidal_signal0, label='1.1 * fs')
plt.plot(t_sin0_1, sinusoidal_signal1, linestyle='--', label='0.1 * fs')
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.ylabel('Amplitud')
plt.title(f'fs: {fs}  - amp: {amp:.2} - samples {samples} - phase: {phase:.3}')
plt.xlim(0, 100 * 1/fs)
plt.legend()

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(t_sin0_49, sinusoidal_signal2, '-o',label='0.49 * fs')
plt.plot(t_sin0_51, sinusoidal_signal3, linestyle='--', label='0.51 * fs')
plt.plot(t_sin0_49C, sinusoidal_signal4, label='0.49 * fsC')
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.ylabel('Amplitud')
plt.xlim(0, 100 * 1/fs)
plt.legend(loc='upper left')


plt.tight_layout()
plt.show()