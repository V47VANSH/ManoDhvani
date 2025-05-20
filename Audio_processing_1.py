from pydub import AudioSegment
import os

# Set your source and output directories
source_dir = "AudioWAV"
output_dir = "Processed_audio_chunks"
os.makedirs(output_dir, exist_ok=True)

def split_audio(file_path):
    filename = os.path.basename(file_path).replace(".wav", "")
    actor_id, sentence_code, emotion_code, emotion_level = filename.split("_")
    
    # Load the audio file
    audio = AudioSegment.from_wav(file_path)
    duration_ms = len(audio)
    
    # Define chunk length (1 second = 1000ms)
    chunk_length = 1000
    
    for i in range(0, duration_ms, chunk_length):
        chunk = audio[i:i+chunk_length]
        
        # Discard chunk if it's less than 1 second
        if len(chunk) < chunk_length:
            continue
        
        # Save chunk with emotion label intact
        chunk_filename = f"{actor_id}_{sentence_code}_{emotion_code}_{emotion_level}_chunk{i//chunk_length}.wav"
        chunk.export(os.path.join(output_dir, chunk_filename), format="wav")

# Process all .wav files in the source directory
for file in os.listdir(source_dir):
    if file.endswith(".wav"):
        split_audio(os.path.join(source_dir, file))
