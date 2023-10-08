import numpy as np
import matplotlib.pyplot as plt
import simpleaudio as sa

# Carga el archivo .npy
senial = np.load('./aux_files/chapu_noise.npy')
# Solicita al usuario el número de elementos a recortar
fs = 8000
audio = senial.astype(np.int16)
play_obj = sa.play_buffer(audio, 1, 2, fs)
play_obj.wait_done()
filterFile = "./aux_files/fir_lp_fc1_5kHz-fs8kHz.npy"

firData = np.load(filterFile).astype(float)
firData = firData[:, 0]
M = len(firData)
N = len(senial) - len(firData) + 1   # Este se calcula como el largo de la FFT elegida MENOS M+1

time = np.arange(0, len(senial))
time = time / fs

# Grafica la señal desconocida en el dominio del tiempo
plt.figure()
plt.plot(time, senial)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.title("Señal Desconocida en el Dominio del Tiempo")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.show()

firExtendedData = np.concatenate((firData, np.zeros(N - 1)))

# --------------------------------------
nData = np.arange(0, N + M - 1, 1)
tData = nData / fs
fData = nData * (fs / (N + M - 1)) - fs / 2
# --------------------------------------
HData = np.fft.fft(firExtendedData)
circularHData = np.abs(np.fft.fftshift(HData / M)) ** 2

# Realiza la multiplicación en el dominio de la frecuencia
spectrum_senial = np.fft.fft(senial)
circularSpectrum_senial = np.abs(np.fft.fftshift(spectrum_senial / M)) ** 2
filtered_spectrum = HData * spectrum_senial
circularFilteredSpectrum = np.abs(np.fft.fftshift(filtered_spectrum / M)) ** 2
plt.subplot(2, 1, 1)
plt.plot(fData, np.abs(circularSpectrum_senial), label="Espectro Original")
plt.plot(fData, circularHData * (np.abs(circularSpectrum_senial).max() / np.abs(circularHData).max()), label="H escalada")
plt.title("Espectro de la Señal")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(fData, np.abs(circularFilteredSpectrum), label="Espectro Filtrado")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.legend()
plt.show()
# Aplica la Transformada Inversa de Fourier para volver al dominio del tiempo
filtered_signal = np.fft.ifft(filtered_spectrum)
filtered_signal = np.real(filtered_signal)

audio = filtered_signal.astype(np.int16)
play_obj = sa.play_buffer(audio, 1, 2, fs)
play_obj.wait_done()

plt.subplot(2, 1, 1)
plt.plot(time, senial)
plt.ylabel("Amplitud")
plt.title("Señal Desconocida en el Dominio del Tiempo")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
# Grafica la señal filtrada en el dominio del tiempo
plt.subplot(2, 1, 2)
plt.plot(time, filtered_signal)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.title("Señal Filtrada en el Dominio del Tiempo")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.show()


