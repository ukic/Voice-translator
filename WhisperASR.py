import pywhisper
from pathlib import Path


def transcribe_pw(file: [Path, str], model):
    result = model.transcribe(file)
    return result["text"]

