import pyaudio
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow

#Substitute 'audio1.wav' with your desired audio file for your project.
audio_file = 'audio1.wav'
p = pyaudio.PyAudio()

host_api_index = 1
stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=44100,
    input=True,
)

app = QApplication([])

main_window = QMainWindow()
plot = PlotWidget()
main_window.setCentralWidget(plot)
line = plot.plot(pen='r')

chunk_size = 1024
buffer = np.zeros(0)

while True:
    app.processEvents()

    data = stream.read(chunk_size)

    buffer = np.append(buffer, data)

    if len(buffer) >= chunk_size:
        chunk = buffer[:chunk_size]
        buffer = buffer[chunk_size:]

        spectrum = np.fft.rfft(chunk)

        line.setData(np.abs(spectrum))

    if not main_window.isVisible():
        break

stream.stop_stream()
stream.close()
p.terminate()

main_window.close()

app.quit()
