# components/audio_input.py

import streamlit as st

def audio_input_section():
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    audio_bytes = None

    if audio_file:
        audio_bytes = audio_file.read()

    return audio_file, audio_bytes