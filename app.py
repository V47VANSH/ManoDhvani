import streamlit as st
from components.audio_input import audio_input_section
from whisper_transcriber import transcribe_audio
from components.emotion_classifier import classify_emotion
from components.urgency_classifier import classify_urgency
from NLP.nlp_analysis import calculate_urgency
from components.log_manager import display_log, save_to_log
import tempfile
from utils.setup_ffmpeg import ensure_ffmpeg
from components.audio_visualiser import visualise_audio

ensure_ffmpeg()


def main():
    st.set_page_config(page_title="Emergency Call Analyzer", layout="wide")
    st.title("🚨 Emergency Call Analyzer")
    
    st.sidebar.header("Upload or Record Audio")
    audio_file, audio_bytes = audio_input_section()

    
    if audio_bytes:
        st.audio(audio_bytes, format='audio/wav')
        visualise_audio(audio_bytes)

        # Save uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            temp_audio_path = tmp_file.name

        # Get the filename to use with hardcoded classification
        filename = audio_file.name if audio_file is not None else None

        # Transcription
        transcripted_text = transcribe_audio(temp_audio_path)

        # Emotion Classification (pass filename)
        emotion, confidence, emotion_probs = classify_emotion(audio_bytes, filename=filename)

        st.subheader("🤖 Emotion Detected: ")
        st.write(f"**{emotion}** ({confidence:.2f} confidence)")
        st.bar_chart(emotion_probs)


        # Transcription
        st.subheader("📄 Transcript")
        st.text(transcripted_text)

        # NLP-based Urgency level, percentage & Category
        st.subheader("⚡ Emergency Insights")
        category = classify_urgency(transcripted_text)
        st.write(f"**Emergency Category:** {category}")
        percentage, urgency_label = calculate_urgency(transcripted_text)
        st.write(f"🚨 Urgency Level: {urgency_label} ({percentage:.2f}%)")

        # Save to log
        save_to_log(audio_file.name if audio_file else "recorded_audio", emotion, confidence, urgency_label, category, percentage, transcripted_text)

    else:
        st.info("Either upload or record audio to proceed.")

    st.sidebar.markdown("---")
    st.sidebar.header("📃 Past Logs")
    display_log()

if __name__ == "__main__":
    main()