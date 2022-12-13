import pywhisper

def speech_to_txt(model_size,path,language):
    model = pywhisper.load_model(model_size)
    result = model.transcribe(path+language)
    with open("text.txt", "w") as text_file:
        text_file.write(result['text'])
        print(result["text"])

model_size = 'tiny'
path = "C:/Users/filip/Desktop/TM/projektII/nagrania/"
language = "EN.wav"

speech_to_txt(model_size, path, language)

print('HELLO')