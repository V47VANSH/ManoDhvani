import whisper

def transcribe_audio(file_path):
    print("🔁 Loading Whisper model...")
    model = whisper.load_model("medium")  # 'base' is faster, 'medium' is more accurate
    print("🎧 Transcribing:", file_path)
    
    result = model.transcribe(file_path)
    text = result['text']
    
    print("\n📄 Transcription:")
    print(text)
    
    return text

if __name__ == "__main__":
    # Add your test file path here
    audio_path = "audio_files/sample_audio.mp4"
    transcribe_audio(audio_path)
