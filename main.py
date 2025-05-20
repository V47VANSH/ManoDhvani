from whisper_transcriber import transcribe_audio
from NLP.nlp_analysis import calculate_urgency_percentage

def process_emergency_audio(file_path):
    text = transcribe_audio(file_path)
    print(f"\n📜 Transcribed Text: {text}")

    percentage, label = calculate_urgency_percentage(text)
    print(f"🚨 Urgency Level: {label} ({percentage:.2f}%)")

    return text, label, percentage

if __name__ == "__main__":
    file = "audio_files/sample_audio.mp4" 
    process_emergency_audio(file)