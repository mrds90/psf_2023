import numpy as np
import matplotlib.pyplot as plt

with open('./aux_files/resolucion_espectral.txt', 'r') as file:
    # Lee el contenido del archivo y se evalúa como una lista
    content = file.read()
    signal = eval(content)

fs = 200  # Frecuencia de muestreo
samples = 100  # Número de muestras
spectral_resolution = fs/samples
t = np.arange(0, samples) / fs

frequencies = np.fft.fftfreq(samples, 1 / fs)
spectral_sign = np.fft.fft(signal)

zero_padding_signal = np.pad(signal, (0, 10 * samples), 'constant') # agrego 10 * sapmles con 0 a signal para aumentar la resolución espectral
zero_padding_samples = len(zero_padding_signal) #numero de samples
zero_padding_t = np.arange(0, zero_padding_samples) / fs
zero_padding_frequencies = np.fft.fftfreq(zero_padding_samples, 1 / fs)
zero_padding_spectral_sign = np.fft.fft(zero_padding_signal)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title("Señal")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

plt.subplot(2, 1, 2)
plt.plot(frequencies, np.abs(spectral_sign))
plt.title("Espectro Señal")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(zero_padding_t, zero_padding_signal)
plt.title("Zero padding Señal")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

plt.subplot(2, 1, 2)
plt.plot(zero_padding_frequencies, np.abs(zero_padding_spectral_sign))
plt.title("Zero padding Espectro Señal")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)


plt.tight_layout()
plt.show()
