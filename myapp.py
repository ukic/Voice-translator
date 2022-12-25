import sys
import pyaudio
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, \
    QLabel, QTextEdit, QButtonGroup
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from tm_master.run_tts import to_speech
from tm_master.run_dictation import transcribe
from pywhisper_asr import transcribe_pw
from wav_manager import read_from_wav, write_to_wav


BUFFER_SIZE = 1024
TYPE = np.float32


class StreamThread(QThread):
    def __init__(self):
        super().__init__()
        self.data = None
        self.cond = True

    def run(self):
        i = 0

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=BUFFER_SIZE)
        data = stream.read(BUFFER_SIZE)
        self.data = np.frombuffer(data, dtype=TYPE)

        while True:
            data = stream.read(BUFFER_SIZE)
            self.data = np.concatenate((self.data, np.frombuffer(data, dtype=TYPE)), axis=0)
            i += 1
            if not self.cond: break
        stream.stop_stream()
        stream.close()
        p.terminate()

    def exit(self, returnCode: int = ...) -> None:
        self.cond = False
        return super(StreamThread, self).exit()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Creating buttons
        self.translations = ['es-en', 'en-es', 'en-pl', 'pl-en', 'es-pl', 'pl-es']
        self.translations_buttons = QButtonGroup()
        self.asr_buttons = QButtonGroup()
        self.rec_button = QPushButton()
        self.stop_button = QPushButton()

        # Creating text widgets
        self.input_textBox = QTextEdit()
        self.status_label = QLabel("Status: Ready")
        self.output_textBox = QTextEdit()
        self.output_textBox.setReadOnly(True)

        # Data loading from stream - thread
        self.cond = True
        self.data_loading_thread = StreamThread()

        # Recorded data
        self.recorded_data = None

        # Paths
        self.input_path = "D:/AGH/TM/VT/input_sound.wav"
        self.output_path = "D:/AGH/TM/VT/output_sound.wav"

        # Translation mode
        self.mode = 'en-pl'

        # Creating app layout
        self.setFixedSize(1000, 800)
        self.create_layout()

    def create_translation_box(self):
        translation_buttons = [QRadioButton(i) for i in self.translations]
        translate_layout = QVBoxLayout()
        translate_layout.setContentsMargins(400, 0, 0, 0)

        self.translations_buttons.setExclusive(True)

        translate_layout.addWidget(QLabel("Translation: "))
        i = 0
        for button in translation_buttons:
            translate_layout.addWidget(button)
            self.translations_buttons.addButton(button, i)
            i += 1

        self.translations_buttons.button(0).setChecked(True)
        return translate_layout

    def create_asr_box(self):
        asr_layout = QVBoxLayout()
        asr_layout.setContentsMargins(0, 20, 0, 20)

        asr_layout.addWidget(QLabel("ASR model: "))
        pw_button = QRadioButton('PyWhisper')
        asr_layout.addWidget(pw_button)

        techmo_asr_button = QRadioButton('Techmo')
        asr_layout.addWidget(techmo_asr_button)
        techmo_asr_button.setChecked(True)

        self.asr_buttons.setExclusive(True)
        self.asr_buttons.addButton(pw_button)
        self.asr_buttons.addButton(techmo_asr_button)

        return asr_layout

    def create_recording_box(self):
        rec_layout = QHBoxLayout()

        self.rec_button.setFixedSize(50, 50)
        self.rec_button.setIcon(QIcon("icons/rec.jpg"))
        rec_layout.addWidget(self.rec_button)
        self.rec_button.clicked.connect(lambda: self.recording_button_clicked())

        self.stop_button.setFixedSize(50, 50)
        self.stop_button.setIcon(QIcon("icons/stop.png"))
        self.stop_button.clicked.connect(lambda: self.stop_button_clicked())
        rec_layout.addWidget(self.stop_button)

        return rec_layout

    def create_text_box(self):
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Input text: "))

        input_layout.addWidget(self.input_textBox)

        play_button = QPushButton()
        play_button.setFixedSize(40, 40)
        play_button.setIcon(QIcon("icons/play.jpg"))
        input_layout.addWidget(play_button)
        input_layout.addWidget(QLabel("Output text: "))

        input_layout.addWidget(self.output_textBox)

        play_button2 = QPushButton()
        play_button2.setFixedSize(40, 40)
        play_button2.setIcon(QIcon("icons/play.jpg"))
        input_layout.addWidget(play_button2)

        input_layout.setContentsMargins(0, 20, 0, 0)
        input_layout.addWidget(self.status_label)
        return input_layout

    def create_layout(self):
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addLayout(self.create_translation_box(), 0, 1, 2, 1)
        layout.addLayout(self.create_asr_box(), 1, 0)
        layout.addLayout(self.create_recording_box(), 0, 0)
        layout.addLayout(self.create_text_box(), 2, 0, 2, 2)

        self.setLayout(layout)

    def set_disabled_buttons(self, val, button_group):
        for button in button_group.buttons():
            button.setDisabled(val)

    def set_addresses(self):
        self.mode = self.translations[self.translations_buttons.checkedId()]

    def recording_button_clicked(self):
        self.status_label.setText("Status: Recording")
        self.set_disabled_buttons(True, self.translations_buttons)
        self.set_disabled_buttons(True, self.asr_buttons)
        self.set_addresses()

        self.data_loading_thread.start()

    def stop_button_clicked(self):
        print(self.data_loading_thread.exit())
        self.recorded_data = self.data_loading_thread.data
        write_to_wav(self.recorded_data, self.input_path)
        self.recognise()

    def recognise(self):
        self.status_label.setText("Status: Recognizing text")
        recognised_text = transcribe_pw(self.input_path)
        self.input_textBox.setPlainText(recognised_text)
        self.translate()

    def translate(self):
        self.status_label.setText("Status: Translating")
        self.output_textBox.setPlainText("Translated text")
        self.end_proccess()

    def end_proccess(self):
        self.status_label.setText("Status: Ready")
        self.set_disabled_buttons(False, self.translations_buttons)
        self.set_disabled_buttons(False, self.asr_buttons)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
