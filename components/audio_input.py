import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import numpy as np
import av
import wave
import tempfile
import os
import datetime

class AudioProcessor:
    def __init__(self):
        self.frames = []
        self.sample_rate = None

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Save sample rate from first frame
        if self.sample_rate is None:
            self.sample_rate = frame.sample_rate
        
        pcm = frame.to_ndarray().flatten()
        self.frames.append(pcm)
        return frame

def audio_input_section():
    st.sidebar.markdown("### 🎙 Upload or Record Audio")

    # File uploader (upload .wav)
    uploaded_file = st.sidebar.file_uploader("Upload a .wav file", type=["wav"])
    if uploaded_file:
        audio_bytes = uploaded_file.read()
        return uploaded_file, audio_bytes

    # Mic recording section
    st.sidebar.markdown("### Or Record Using Microphone")

    audio_processor = AudioProcessor()
    ctx = webrtc_streamer(
        key="audio_recorder",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"audio": True, "video": False},
        audio_processor_factory=lambda: audio_processor,
        async_processing=True,
    )

    st.sidebar.write(f"Recording state: {ctx.state}")
    st.sidebar.write(f"Frames captured: {len(audio_processor.frames)}")

    if ctx.state == "STOPPED" and audio_processor.frames:
        pcm_audio = np.concatenate(audio_processor.frames).astype(np.int16)
        sample_rate = audio_processor.sample_rate or 16000  # fallback to 16kHz

        # Create a temp wav file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            with wave.open(tmpfile.name, "wb") as wf:
                wf.setnchannels(1)  # mono audio
                wf.setsampwidth(2)  # 2 bytes per sample for int16
                wf.setframerate(sample_rate)
                wf.writeframes(pcm_audio.tobytes())
            tmp_path = tmpfile.name
        
        # Ensure save directory exists
        save_path = os.path.join("data", "recordings")
        os.makedirs(save_path, exist_ok=True)

        # Use timestamped filename to avoid overwrite
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"mic_recorded_audio_{timestamp}.wav"
        final_path = os.path.join(save_path, final_filename)
        os.rename(tmp_path, final_path)

        # Read audio bytes
        with open(final_path, "rb") as f:
            audio_bytes = f.read()

        return final_filename, audio_bytes

    # Return None if no audio yet
    return None, None
