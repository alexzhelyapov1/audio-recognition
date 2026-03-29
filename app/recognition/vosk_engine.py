import os
import json
import re
import wave
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer

# Configuration
MODEL_PATH = os.environ.get('VOSK_MODEL_PATH', 'model')
# Note: Ensure the VOSK Russian model is downloaded and extracted to the 'model/' directory in the project root.

class SpeechRecognizer:
    _model = None

    def __init__(self):
        if SpeechRecognizer._model is None:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"VOSK model not found at {MODEL_PATH}. Please download it from https://alphacephei.com/vosk/models")
            SpeechRecognizer._model = Model(MODEL_PATH)
        
        self.commands = [
            "зарегистрировать",
            "начать обработку",
            "отменить обработку",
            "отменить регистрацию",
            "завершить обработку"
        ]

    def convert_to_wav(self, input_path):
        """Converts input audio to WAV Mono 16kHz for VOSK."""
        output_path = input_path.rsplit('.', 1)[0] + ".wav"
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        audio.export(output_path, format="wav")
        return output_path

    def transcribe(self, wav_path):
        """Transcribes WAV file using VOSK."""
        wf = wave.open(wav_path, "rb")
        rec = KaldiRecognizer(SpeechRecognizer._model, wf.getframerate())
        rec.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))
        
        results.append(json.loads(rec.FinalResult()))
        wf.close()
        
        full_text = " ".join([res.get('text', '') for res in results]).strip()
        return full_text

    def parse_command(self, text):
        """Extracts command and identifier from text using Regex."""
        text_lower = text.lower()
        
        found_command = None
        for cmd in self.commands:
            if cmd in text_lower:
                # Capitalize the first letter for display
                found_command = cmd.capitalize()
                break
        
        # Regex for ID: 8 digits OR Alphanumeric combinations
        # Looking for 8-digit sequence
        digit_id_match = re.search(r'\b\d{8}\b', text_lower)
        # Looking for alphanumeric (at least one letter and one digit, e.g., P45345ИВ)
        # We also need to handle cases where there are mixed Russian/English letters
        alpha_num_match = re.search(r'\b[a-zA-Zа-яА-Я]+\d+[a-zA-Zа-яА-Я\d]*\b|\b\d+[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я\d]*\b', text_lower)
        
        found_id = None
        if digit_id_match:
            found_id = digit_id_match.group(0)
        elif alpha_num_match:
            found_id = alpha_num_match.group(0).upper()
            
        return found_command, found_id

# Usage example:
# recognizer = SpeechRecognizer()
# wav = recognizer.convert_to_wav("audio.webm")
# text = recognizer.transcribe(wav)
# cmd, id_val = recognizer.parse_command(text)
