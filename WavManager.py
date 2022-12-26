import numpy as np
from pathlib import Path
from scipy.io.wavfile import write, read
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa

TYPE = np.float32


def write_to_wav(data: np.ndarray, output_path: [Path, str], fs: int = 44100):
    write(output_path, fs, data)
    return


def read_from_wav(path: [Path, str]):
    fs, data = read(path)
    return fs, np.ndarray(data, dtype=TYPE)


def play_wav(path: [Path, str]):
    sound = AudioSegment.from_wav(path)
    play(sound)

def play_np(data: np.ndarray, fs:int = 44100):
    play_obj = sa.play_buffer(data, 2, 2, fs)
    play_obj.wait_done()

