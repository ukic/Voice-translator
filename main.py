import pywhisper
import numpy as np
from timeit import default_timer as timer
from scipy.io.wavfile import read, write
import simpleaudio as sa
import wave  

def speech_to_txt_GPU(model_size,path,language):
    model = pywhisper.load_model(model_size)
    result = model.transcribe(path+language)
    with open("text.txt", "w") as text_file:
        text_file.write(result['text'])
        print(result["text"])
        
def speak(path,language):
    wave_read = wave.open(path+language, 'rb')
    wave_obj = sa.WaveObject.from_wave_read(wave_read)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    

if __name__=="__main__":
    
    model_size = 'base'
    path = "C:/Users/filip/Desktop/TM/projektII/nagrania/"
    language = "EN.wav"    
      
    start = timer()
    speech_to_txt_GPU(model_size, path, language)
    print("with GPU:", timer()-start)
    
    speak(path,language)