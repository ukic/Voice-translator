import pywhisper
import numpy as np
from timeit import default_timer as timer
import simpleaudio as sa
import wave
import librosa, pyaudio


def load_wav(path: str, fs: int = None):
    return librosa.load(path, fs)[0]

def load_from_stream():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=BUFFER_SIZE)
    data = stream.read(BUFFER_SIZE)
    rec_data = np.frombuffer(data, dtype=np.int16)
    for i in range(200):
        data = stream.read(BUFFER_SIZE)
        rec_data = np.concatenate((rec_data, np.frombuffer(data, dtype=np.int16)), axis=0)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return rec_data
    
def speech_to_txt_GPU(recording, model_size):
    model = pywhisper.load_model(model_size)
    recording = pywhisper.pad_or_trim(recording)
    mel = pywhisper.log_mel_spectrogram(recording).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    options = pywhisper.DecodingOptions()
    result = pywhisper.decode(model, mel, options)
    print(result.text)
    # with open("text.txt", "w") as text_file:
    #     text_file.write(result['text'])
    #     print(result["text"])
        
def speak(path,language):
    wave_read = wave.open(path+language, 'rb')
    wave_obj = sa.WaveObject.from_wave_read(wave_read)
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__=="__main__":
    
    BUFFER_SIZE = 1024
    model_size = 'small'
    recording = load_from_stream().astype(np.float32)
    
    start = timer()
    speech_to_txt_GPU(recording, model_size)
    print("with GPU:", timer()-start)
