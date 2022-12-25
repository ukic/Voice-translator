import numpy as np
from pathlib import Path
from scipy.io.wavfile import write, read

TYPE = np.float32


def write_to_wav(data: np.ndarray, output_path: [Path, str], fs: int = 44100):
    write(output_path, fs, data)
    return


def read_from_wav(path: [Path, str]):
    fs, data = read(path)
    return fs, np.ndarray(data, dtype=TYPE)

