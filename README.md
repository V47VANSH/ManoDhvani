🚨 Emergency Call Analyzer
A real-time voice analysis tool designed for emergency response systems. This dashboard captures and analyzes audio from distress/emergency calls, classifies the speaker's emotional state, identifies urgency levels, transcribes speech to text, and categorizes the situation (e.g., medical, fire, crime, domestic abuse, accident, mental health) — all within a unified and intuitive interface.

🔍 Features
🎙️ Audio Input: Record voice directly via microphone or upload .wav audio files.

📊 Audio Visualization: Real-time waveform and frequency visualizations as seen in control rooms.

🤖 Emotion Detection: Deep learning-based emotion classifier trained on short audio chunks.

🔈 Speech Transcription: Converts speech to text using automatic speech recognition (ASR).

🚨 Emergency Categorization: Classifies calls into categories such as Medical, Crime, Fire, Domestic Abuse, Accident, or Mental Health based on transcribed keywords.

📈 Visual Dashboard: Bar chart visualizations of emotion probabilities and dynamic summaries for quick decision making.

📝 Logging: Dashboard maintains an internal log for test/demo calls, aiding responders or analysts.

🧠 ML/DL Architecture
The backend pipeline consists of:

🎧 Audio Preprocessing
Incoming .wav files are split into 1-second chunks using pydub.

Silent or incomplete chunks are discarded to maintain quality.

🎼 Feature Extraction
Mel-frequency cepstral coefficients (MFCCs), chroma, and zero-crossing rate features are extracted from each chunk using librosa and numpy.

Resulting feature vectors are fed into the classifier model.

🤖 Emotion Classifier
A deep learning model (e.g., CNN or LSTM) trained on multi-class labeled emergency call data.

Trained to recognize 6 emotions: Neutral, Angry, Fear, Distress, Happy, and Sad.

💻 Installation & Running Locally
git clone https://github.com/yourusername/emergency-call-analyzer.git
cd emergency-call-analyzer
pip install -r requirements.txt
python app.py
If you're on Windows and FFmpeg isn't globally installed, setup_ffmpeg.py automatically loads a bundled copy — no manual setup needed.

📦 Dependencies
streamlit

pydub

numpy, scipy, pandas

librosa

whisper or speechrecognition (for transcription)

matplotlib, plotly (for audio visualization)

🎯 Use Case
This dashboard is ideal for emergency service control rooms or mental health helplines. It helps prioritize calls based on emotional distress or urgency category, enhancing real-time decision-making.
