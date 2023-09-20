import numpy as np
import matplotlib.pyplot as plt

# Carga el archivo .npy
espectro_desconocido = np.load('./aux_files/fft_hjs.npy')
# Solicita al usuario el número de elementos a recortar
corte = int(input("Frecuencia de corte: "))

# Calcula los índices de inicio y fin para el recorte
inicio = 0 + int(corte)
fin = len(espectro_desconocido) - int(corte)

# Crea un nuevo espectro sin los elementos recortados
if (corte >= len(espectro_desconocido)/2):
    nuevo_espectro_desconocido = espectro_desconocido
else: 
    nuevo_espectro_desconocido = np.delete(espectro_desconocido, range(inicio, fin))

# Calcula la iFFT para obtener la señal en el dominio del tiempo
señal_desconocida = np.fft.ifft(nuevo_espectro_desconocido)



plt.figure()
plt.plot(nuevo_espectro_desconocido.real) #grafica parte real vs parte imaginaria de la señal
plt.plot(nuevo_espectro_desconocido.imag) #grafica parte real vs parte imaginaria de la señal
plt.xlabel("Frec")
plt.ylabel("Amplitud")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.show()

# Grafica la señal desconocida en 2D
plt.figure()
plt.scatter(señal_desconocida.imag,señal_desconocida.real) #grafica parte real vs parte imaginaria de la señal
plt.title("Señal Desconocida en el Dominio del Tiempo")
plt.xlabel("real")
plt.ylabel("imag")
plt.grid(True, linestyle='-', alpha=0.9)
plt.minorticks_on()
plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
plt.show()

