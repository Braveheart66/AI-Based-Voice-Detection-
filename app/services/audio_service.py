import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

from app.services.fraud_service import detect_fraud


def convert_to_wav(input_path: str) -> str:
    audio = AudioSegment.from_file(input_path)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(tmp.name, format="wav")
    return tmp.name


def audio_to_text(file_path: str) -> str:
    r = sr.Recognizer()

    try:
        wav_path = convert_to_wav(file_path)

        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)

        text = r.recognize_google(audio)
        os.remove(wav_path)
        return text

    except sr.UnknownValueError:
        return ""  # no speech detected

    except Exception as e:
        print("AUDIO ERROR:", e)
        return ""


def detect_fraud_from_audio(file_path: str):
    text = audio_to_text(file_path)

    if not text:
        return {
            "fraud": False,
            "confidence": 0.0,
            "reason": "Could not understand audio",
            "source": "speech-recognition"
        }

    return detect_fraud(text, language="en")
