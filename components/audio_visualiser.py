import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import io
import soundfile as sf


def visualise_audio(audio_bytes):
    # Load audio from bytes
    audio_data, sr = sf.read(io.BytesIO(audio_bytes))
    
    # If stereo, convert to mono
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)

    # Plot waveform
    st.subheader("📉 Waveform (Amplitude over Time)")
    fig_waveform, ax_wave = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(audio_data, sr=sr, ax=ax_wave)
    ax_wave.set_xlabel("Time (s)")
    ax_wave.set_ylabel("Amplitude")
    st.pyplot(fig_waveform)

    # Plot spectrogram
    st.subheader("🌈 Spectrogram (Frequency over Time)")
    X = librosa.stft(audio_data)
    X_db = librosa.amplitude_to_db(np.abs(X))

    fig_spec, ax_spec = plt.subplots(figsize=(10, 3))
    img = librosa.display.specshow(X_db, sr=sr, x_axis='time', y_axis='hz', ax=ax_spec, cmap='magma')
    fig_spec.colorbar(img, ax=ax_spec, format="%+2.0f dB")
    st.pyplot(fig_spec)
