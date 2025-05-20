import whisper
from utils.setup_ffmpeg import ensure_ffmpeg

ensure_ffmpeg()

model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result['text']
