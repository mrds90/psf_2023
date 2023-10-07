
    
import numpy as np
import simpleaudio as sa
import serial
import threading
import matplotlib.pyplot as plt

# Parámetros de la señal de audio
f_audio = 400                                           # Frecuencia de la señal de audio en Hz
fs_audio = 44100                                        # Frecuencia de muestreo de la señal de audio en Hz
sec = 2                                                 # Duración de la señal de audio en segundos
t_audio = np.arange(0, sec, 1/fs_audio)                 # Vector de tiempo
note = (2**15-1)*np.sin(2 * np.pi * f_audio * t_audio)  # Tono senoidal puro a frecuencia f_audio
audio_signal = note.astype(np.int16)                    # Señal de audio

# Función para generar y reproducir la señal de audio
def play_audio():
    while(True):
        play_obj = sa.play_buffer(audio_signal, 1, 2, fs_audio)
        play_obj.wait_done()

# Función para recibir datos del ADC y graficarlos
def receive_and_plot_data():
    ADC_MAX_SAMPLE_RATE = 400000
    ser = serial.Serial('/dev/ttyUSB1', 460800) 
    while(True):
        buffer_size = len(t_audio)
        time_buffer = list()
        data_buffer = list()
        print("ReadInit")
        sync_state = "esperando_sincronizacion"
        sync_byte = 0xA5
        time_recorded = 0
        while time_recorded < 2:
            # Leer un byte desde el puerto serie
            data_byte = ser.read(1)[0]  # El [0] extrae el valor numérico del byte
            
            if sync_state == "esperando_sincronizacion":
                if data_byte == sync_byte:
                    sync_state = "esperando_byte_alto"
            
            elif sync_state == "esperando_byte_alto":
                if data_byte == sync_byte:
                    sync_state = "esperando_byte_alto"
                else: 
                    byte_alto = data_byte
                    sync_state = "esperando_byte_bajo"

            
            elif sync_state == "esperando_byte_bajo":
                if data_byte == sync_byte:
                    sync_state = "esperando_byte_alto"
                else: 
                    byte_bajo = data_byte
                    # Combinar los dos bytes para obtener el valor de 16 bits en big-endian
                    bytes_buff= [byte_alto,byte_bajo]
                    data_value = int.from_bytes(bytes_buff, "big", signed=True)
                    # Escalar el valor de datos
                    value = data_value * 3.3 / 1024
                    # Agregar el valor al búfer de datos
                    data_buffer.append(value)
                    time_buffer.append(len(data_buffer) / (ADC_MAX_SAMPLE_RATE / 64))
                    time_recorded = time_buffer[-1]
                    # Restablecer el estado de sincronización
                    sync_state = "esperando_sincronizacion"
            

            # Calcular el tiempo basado en la frecuencia de muestreo

            # Crear una nueva figura para la gráfica de datos adquiridos
        max_value_adquirida = max(data_buffer)
        min_value_adquirida = min(data_buffer)
        rms_adquirida = np.sqrt(np.mean(np.array(data_buffer) ** 2))

        # Calcular el máximo, mínimo y RMS de la señal original
        original_signal = audio_signal * 1.65 / 32766
        max_value_original = max(original_signal)
        min_value_original = min(original_signal)
        rms_original = np.sqrt(np.mean(original_signal ** 2))

        # Imprimir los valores calculados
        print("Máximo señal original:", max_value_original)
        print("Máximo señal adquirida:", max_value_adquirida)
        print("Mínimo señal original:", min_value_original)
        print("Mínimo señal adquirida:", min_value_adquirida)
        print("RMS señal original:", rms_original)
        print("RMS señal adquirida:", rms_adquirida)

        plt.clf()
        plt.plot(time_buffer, data_buffer, label="recorded")
        plt.plot(t_audio, original_signal, label="original")
        plt.xlim([0, 2/f_audio])
        # plt.ylim([-10,10])
        plt.xlabel('Tiempo (segundos)')
        plt.ylabel('Valor')
        plt.title('Datos adquiridos')
        plt.legend()
        plt.grid(True, linestyle='-', alpha=0.9)
        plt.minorticks_on()
        plt.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)
        plt.tight_layout()
        plt.pause(0.1)
        del data_buffer
    



# Crear hilos para la reproducción de audio y la recepción de datos
fig = plt.figure()
data_thread = threading.Thread(target=receive_and_plot_data)
audio_thread = threading.Thread(target=play_audio)

# Iniciar los hilos
audio_thread.start()
data_thread.start()
# Esperar a que ambos hilos terminen (esto no debería ocurrir en este caso)
audio_thread.join()
data_thread.join()
plt.show()