import librosa, pyaudio
import numpy as np

BUFFER_SIZE = 1024


def load_wav(path: str, fs: int = None):
    return librosa.load(path, fs)[0]


def load_from_stream():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=BUFFER_SIZE)
    data = stream.read(BUFFER_SIZE)
    rec_data = np.frombuffer(data, dtype=np.int16)
    for i in range(10):
        data = stream.read(BUFFER_SIZE)
        rec_data = np.concatenate((rec_data, np.frombuffer(data, dtype=np.int16)), axis=0)

    stream.stop_stream()
    stream.close()
    p.terminate()


load_from_stream()
