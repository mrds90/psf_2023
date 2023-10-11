import numpy as np
import simpleaudio as sa
import serial
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from queue import Queue






VOLTAGE = "VOLTAGE"
PEAKS   = "PEAKS"

mode = VOLTAGE





# Parámetros de la señal de audio
f_audio = 10  # Frecuencia de la señal de audio en Hz
fs_audio = 44100  # Frecuencia de muestreo de la señal de audio en Hz
sec = 0.7  # Duración total de la señal de audio en segundos

# Duración del tono senoidal (un ciclo)
tone_duration = 1 / f_audio  # Duración de un ciclo de la señal senoidal
silence_duration = sec - tone_duration  # Duración del silencio en segundos

# Generar el tono senoidal
t_tone = np.arange(0, tone_duration, 1/fs_audio)
tone = (2**15-1) * np.sin(2 * np.pi * f_audio * t_tone)

# Generar el silencio
silence = np.zeros(int(silence_duration * fs_audio), dtype=np.int16)

# Combinar el tono y el silencio
audio_signal = np.concatenate((tone, silence))

# Generar el vector de tiempo para la señal
t_audio = np.arange(0, sec, 1/fs_audio)

# Inicializar una cola para transmitir datos entre hilos
data_queue = Queue()

# Función para generar y reproducir la señal de audio
def play_audio():
    while True:
        play_obj = sa.play_buffer(audio_signal, 1, 2, fs_audio)
        play_obj.wait_done()

# Función para recibir datos del ADC y ponerlos en la cola
def receive_data():
    ADC_MAX_SAMPLE_RATE = 400000
    ser = serial.Serial('/dev/ttyUSB2', 460800) 
    while True:
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
                    byte_alto = data_byte
                    sync_state = "esperando_byte_bajo"

            
            elif sync_state == "esperando_byte_bajo":
                    byte_bajo = data_byte
                    # Combinar los dos bytes para obtener el valor de 16 bits en big-endian
                    bytes_buff= [byte_alto,byte_bajo]
                    data_value = int.from_bytes(bytes_buff, "big", signed=True)
                    # Escalar el valor de datos
                    value = data_value
                    if (mode == PEAKS):
                        if data_value <= 0:
                             data_value = 0
                    value = data_value * 3.3 / 1024
                    # Agregar el valor al búfer de datos
                    data_buffer.append(value)
                    time_buffer.append(len(data_buffer) / (ADC_MAX_SAMPLE_RATE / 400))
                    time_recorded = time_buffer[-1]
                    # Restablecer el estado de sincronización
                    sync_state = "esperando_sincronizacion"

        # Colocar los datos en la cola para la gráfica
        data_queue.put((time_buffer, data_buffer, audio_signal * 1.65 / 32766))

# Clase para la ventana de gráficos
class DataPlot(QWidget):
    def __init__(self):
        super().__init__()

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 2)
        if (mode == PEAKS):
            self.ax.set_ylim(0, 1.7)
        if (mode == VOLTAGE):
            self.ax.set_ylim(-1.7, 1.7)

        self.ax.set_xlabel('Tiempo (segundos)')
        self.ax.set_ylabel('Valor')
        self.ax.set_title('Datos adquiridos')
        self.line1, = self.ax.plot([], [], label="recorded")
        # self.line2, = self.ax.plot([], [], label="original")
        self.ax.legend()
        self.ax.grid(True, linestyle='-', alpha=0.9)
        self.ax.minorticks_on()
        self.ax.grid(which='minor', linestyle='--', linewidth='0.5', alpha=0.8)

        self.ani = FuncAnimation(self.fig, self.animate, blit=False)
        

    def animate(self, frame):
        if not data_queue.empty():
            time_buffer, data_buffer, original_signal = data_queue.get()
            self.line1.set_data(time_buffer, data_buffer)
            # self.line2.set_data(t_audio, original_signal)

        self.fig.canvas.flush_events()

# Función principal
def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setGeometry(100, 100, 800, 600)
    central_widget = DataPlot()
    main_window.setCentralWidget(central_widget)
    main_window.show()

    # audio_thread = threading.Thread(target=play_audio)
    data_thread = threading.Thread(target=receive_data)

    data_thread.start()
    # audio_thread.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()