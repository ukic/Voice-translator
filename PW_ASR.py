import pywhisper


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