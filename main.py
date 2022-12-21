import numpy as np
from timeit import default_timer as timer
from data_loading import load_from_stream
from PW_ASR import speech_to_txt_GPU


model_size = 'small'
recording = load_from_stream().astype(np.float32)

start = timer()
speech_to_txt_GPU(recording, model_size)
print("with GPU:", timer()-start)
