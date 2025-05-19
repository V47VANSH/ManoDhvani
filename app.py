import streamlit as st
from components.audio_input import audio_input_section
from components.emotion_classifier import classify_emotion
from components.transcription import transcribe_audio
from components.urgency_classifier import classify_urgency
from components.log_manager import display_log, save_to_log

def main():
    st.set_page_config(page_title="Emergency Call Emotion Dashboard", layout="wide")
    st.title("🚨 Emergency Call Analyzer")

    st.sidebar.header("Upload or Record Audio")
    audio_file, audio_bytes = audio_input_section()

    if audio_file:
        st.audio(audio_bytes, format='audio/wav')

        # Emotion Classification
        emotion, confidence, emotion_probs = classify_emotion(audio_bytes)
        st.subheader("👀 Emotion Detected: ")
        st.write(f"**{emotion}** ({confidence:.2f} confidence)")
        st.bar_chart(emotion_probs)

        # Transcription
        transcript = transcribe_audio(audio_bytes)
        st.subheader("📄 Transcript")
        st.text(transcript)

        # NLP-based Urgency & Category
        urgency, category = classify_urgency(transcript, emotion)
        st.subheader("⚡ Emergency Insights")
        st.write(f"**Urgency Level:** {urgency}")
        st.write(f"**Emergency Category:** {category}")

        # Save to log
        save_to_log(audio_file.name, emotion, confidence, urgency, category, transcript)

    st.sidebar.markdown("---")
    st.sidebar.header("📃 Past Logs")
    display_log()

if __name__ == "__main__":
    main()