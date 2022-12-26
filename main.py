"""
import numpy as np
from timeit import default_timer as timer
from data_loading import load_from_stream
from PW_ASR import speech_to_txt_GPU
from translation.my_main import Translate_easy

model_size = 'small'
recording = load_from_stream().astype(np.float32)

start = timer()
speech_to_txt_GPU(recording, model_size)
print("with GPU:", timer()-start)

print(Translate_easy("es", "Bardzo chciałbym podziękować za obecny rok, jesteście wszyscy niesamowici."))
print(Translate_easy("es", "How are you today?"))
print(Translate_easy("pl", "Como estas?"))
"""


from MyApp import MyApp
import sys
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec())

