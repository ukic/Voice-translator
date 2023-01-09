import numpy as np
import pyaudio
from PyQt5.QtCore import QThread


BUFFER_SIZE = 1024
TYPE = np.float32


class StreamThread(QThread):
    def __init__(self):
        super().__init__()
        self.data = None
        self.cond = True

    def run(self):
        i = 0
        self.cond = True

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=BUFFER_SIZE)
        data = stream.read(BUFFER_SIZE)
        self.data = np.frombuffer(data, dtype=TYPE)

        while True:
            data = stream.read(BUFFER_SIZE)
            self.data = np.concatenate((self.data, np.frombuffer(data, dtype=TYPE)), axis=0)
            i += 1
            if not self.cond: break
        stream.stop_stream()
        stream.close()
        p.terminate()

    def exit(self, returnCode: int = ...) -> None:
        self.cond = False
        return super(StreamThread, self).exit()