# components/transcription.py

import whisper
import tempfile
import os

# Load the model only once (you can use 'base', 'small', 'medium', or 'large')
model = whisper.load_model("base")

def transcribe_audio(audio_bytes):
    # Save the audio bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name

    try:
        # Run transcription
        result = model.transcribe(tmp_path)
        transcript = result.get("text", "")
    except Exception as e:
        transcript = f"[Error during transcription: {str(e)}]"
    finally:
        os.remove(tmp_path)

    return transcript