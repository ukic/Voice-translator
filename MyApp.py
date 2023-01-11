import os
import numpy as np
from PyQt5.QtWidgets import QWidget, QRadioButton, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, \
    QLabel, QTextEdit, QButtonGroup, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

from StreamThread import StreamThread
from WavManager import write_to_wav, play_wav
from WhisperASR import transcribe_pw

from translation.run_translation import translate_easy
from tm_master.run_tts import to_speech, run_tts_function
from tm_master.run_dictation import transcribe
import pywhisper

BUFFER_SIZE = 1024
TYPE = np.float32


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Menu bar
        self.menuBar = QMenuBar()

        # Creating buttons
        self.translations = ['en-es', 'en-pl', 'es-en', 'es-pl', 'pl-en', 'pl-es']
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
        self.recorded_text = None
        self.translated_text = None

        # Models
        self.asr_model_pywhisper = pywhisper.load_model("small")

        # Paths
        self.input_path = "input_sound.wav"
        self.output_path = "output_sound.wav"

        # Translation mode
        self.mode = 'en-pl'

        #initializing models
        self.initialized = False

        # Error message box
        self.error_message_box = QMessageBox()
        self.error_message_box.setIcon(QMessageBox.Critical)
        self.error_message_box.setText("Error")

        # Creating app layout
        self.setFixedSize(1000, 800)
        self.setWindowTitle("Voice Translator")
        self.setWindowIcon(QIcon("icons/mic.png"))
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

        self.translations_buttons.button(1).setChecked(True)
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
        play_button.clicked.connect(lambda: run_tts_function(self.mode[0:2], self.recorded_text))
        input_layout.addWidget(play_button)
        input_layout.addWidget(QLabel("Output text: "))

        input_layout.addWidget(self.output_textBox)

        play_button2 = QPushButton()
        play_button2.setFixedSize(40, 40)
        play_button2.setIcon(QIcon("icons/play.jpg"))
        play_button2.clicked.connect(lambda: self.play_button_clicked(self.output_path))
        input_layout.addWidget(play_button2)

        input_layout.setContentsMargins(0, 20, 0, 0)
        input_layout.addWidget(self.status_label)
        return input_layout

    def create_menu_bar(self):
        file_menu = QMenu("&File", self)

        set_ins_path_action = QAction("&Choose input sound path...", self)
        set_ins_path_action.triggered.connect(self.set_input_address)
        file_menu.addAction(set_ins_path_action)

        set_outs_path_action = QAction("&Choose output sound path...", self)
        set_outs_path_action.triggered.connect(self.set_output_address)
        file_menu.addAction(set_outs_path_action)

        self.menuBar.addMenu(file_menu)

    def create_layout(self):
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.create_menu_bar()

        layout.addLayout(self.create_translation_box(), 0, 1, 2, 1)
        layout.addLayout(self.create_asr_box(), 1, 0)
        layout.addLayout(self.create_recording_box(), 0, 0)
        layout.addLayout(self.create_text_box(), 2, 0, 2, 2)
        layout.setMenuBar(self.menuBar)

        self.setLayout(layout)

    def set_disabled_buttons(self, val, button_group):
        for button in button_group.buttons():
            button.setDisabled(val)

    def set_addresses(self):
        self.mode = self.translations[self.translations_buttons.checkedId()]

    def play_button_clicked(self, path):
        play_wav(path)

    def set_input_address(self):
        self.input_path = self.get_address()

    def set_output_address(self):
        self.output_path = self.get_address()

    def get_address(self):
        file_filter = 'Data File (*.wav)'
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select path',
            directory=os.getcwd(),
            filter=file_filter,
        )
        print(response)
        return response[0]

    def recording_button_clicked(self):
        self.status_label.setText("Status: Recording")
        self.set_disabled_buttons(True, self.translations_buttons)
        self.set_disabled_buttons(True, self.asr_buttons)
        self.set_addresses()

        try:
            self.data_loading_thread.start()
        except IOError:
            self.end_proccess()
            self.display_error_message("Error while recording occured")
        except RuntimeError:
            self.end_proccess()
            self.display_error_message("Error with recording thread occured")

    def stop_button_clicked(self):
        self.data_loading_thread.exit()
        self.recorded_data = self.data_loading_thread.data
        try:
            write_to_wav(self.recorded_data, self.input_path)
            self.recognise()
        except Exception:
            self.end_proccess()
            self.display_error_message("Error with writing to wav file occurred")

    def recognise(self):
        self.status_label.setText("Status: Recognising text")
        if self.asr_buttons.checkedId() == -3:
            try:
                self.recorded_text = transcribe("asr-" + self.mode[:2], self.input_path)
                self.input_textBox.setPlainText(self.recorded_text)
                self.translate()
            except Exception:
                self.end_proccess()
                self.display_error_message("Error with Techmo asr occurred. Try Whisper model")
        else:
            try:
                self.recorded_text = transcribe_pw(self.input_path, self.asr_model_pywhisper)
                self.input_textBox.setPlainText(self.recorded_text)
                self.translate()
            except Exception:
                self.end_proccess()
                self.display_error_message("Error with Whisper model occurred. Try again")

    def translate(self):
        self.status_label.setText("Status: Translating")
        if not self.initialized:
            self.initialize_models()
        try:
            self.translated_text = translate_easy(self.mode[3:5], self.mode[0:2], self.recorded_text)
            self.output_textBox.setPlainText(self.translated_text)
            try:
                to_speech("tts-" + self.mode[3:5], self.translated_text, self.output_path)
                self.end_proccess()
            except Exception:
                self.end_proccess()
                self.display_error_message("Error with Techmo tts occurred")
        except Exception:
            self.end_proccess()
            self.display_error_message("Error with translation occurred")

    def initialize_models(self):
        for t_pair in self.translations:
            translate_easy(t_pair[3:5], t_pair[0:2], "hi")
        self.initialized = True

    def end_proccess(self):
        self.status_label.setText("Status: Ready")
        self.set_disabled_buttons(False, self.translations_buttons)
        self.set_disabled_buttons(False, self.asr_buttons)

    def display_error_message(self, error_message: str):
        self.error_message_box.setInformativeText(error_message)
        self.error_message_box.exec()
