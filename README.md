# 🚨 Emergency Call Analyzer

**A real-time voice analysis dashboard for emergency response systems**

This tool captures and analyzes audio from distress/emergency calls, classifies the speaker's **emotional state**, detects **urgency categories**, transcribes **speech to text**, and identifies potential emergency types — all within a unified and intuitive interface.

---

## 🔍 Features

- 🎙️ **Audio Input**  
  Record voice via microphone or upload `.wav` audio files.

- 📊 **Audio Visualization**  
  Real-time waveform and frequency plots — like those seen in control rooms.

- 🤖 **Emotion Detection**  
  Deep learning-based emotion classifier trained on extracted audio features.

- 🔈 **Speech Transcription**  
  Converts speech to text using automatic speech recognition (ASR).

- 🚨 **Emergency Categorization**  
  Classifies the call into:  
  `Medical`, `Crime`, `Fire`, `Domestic Abuse`, `Accident`, or `Mental Health`  
  based on keywords found in the transcript.

- 📈 **Visual Dashboard**  
  Bar chart visualizations of emotion probabilities with urgency summary.

- 📝 **Logging System**  
  Keeps a structured log of all test/demo calls for quick reference and audits.

---

## 🧠 ML/DL Architecture

### 🎧 Audio Preprocessing
- Uploaded or recorded `.wav` files are split into 1-second segments using `pydub`.
- Silent or noisy chunks are filtered out to maintain input quality.

### 🎼 Feature Extraction
- Each chunk is transformed into a numerical vector using:
  - **MFCCs (Mel-Frequency Cepstral Coefficients)**
  - **Chroma Features**
  - **Zero-Crossing Rate**
- Implemented via `librosa` and `numpy`.

### 🤖 Emotion Classification
- A trained **deep learning model** (e.g., CNN or LSTM) processes the extracted features.
- Recognizes the following 6 emotional states:
  - `Neutral`, `Angry`, `Fear`, `Distress`, `Happy`, `Sad`
- Outputs:
  - Predicted emotion
  - Confidence score
  - Emotion distribution (for visualization)

---

## 📦 Installation & Running Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/emergency-call-analyzer.git
cd emergency-call-analyzer
```

### 2️⃣ Install the dependencies

```bash
pip install -r requirements.txt
```

3️⃣ Run the Streamlit app
```bash
python -m streamlit run app.py
```

🪟 On Windows and facing FFmpeg issues?
Run the following to use the bundled version automatically:

```bash
python setup_ffmpeg.py
```


## 🖼️ Project Screenshots

### 🎛️ Home - Audio Input  
![Main Dashboard](assets/audio_upload.png)

### 📈 Emotion - Detection  
![Emotion - Fear](assets/fear.png)
![Emotion - Neutral](assets/neutral.png)
![Emotion - Angrys](assets/angry.png)

### 📋 Transcription and Categorization  
![Transcription and Categorization](assets/transcript&emergency_insights.png)

### 📋 Waveform Visualisation  
![Waveform Visualisation](assets/waveform.png)

### 📋 Spectogram Visualisation
![Spectogram Visualisation](assets/spectogram.png)

### 📋 Call Logs For Record
![Call Logs For Record](assets/logs.png)


## 🎯 Use Case

This project is tailored for:

- Emergency service control rooms (e.g., 112/911 centers)
- Mental health helplines
- Voice surveillance in smart city frameworks
- Field testing and research in crisis communication

By identifying emotional distress and matching context to predefined urgency categories, responders are better equipped to prioritize calls effectively.

---

## 🚀 Features

- 🎤 Audio Upload & Recording  
- 🧠 Real-time Emotion Detection  
- 🗣️ Automatic Speech Transcription  
- 🏷️ Keyword-based Urgency Categorization  
- 📊 Visualized Emotion Probabilities  
- 📁 Simple UI built using [Streamlit](https://streamlit.io)

---

## ⚙️ Tech Stack

- **Voice Feature Extraction**: `librosa`, `pydub`  
- **Transcription**: OpenAI Whisper / `SpeechRecognition`  
- **Emotion Model**: Custom-trained deep learning model  
- **UI/UX**: `Streamlit`  
- **Audio Handling**: Optional FFmpeg setup for Windows (`setup_ffmpeg.py`)

---

## 🤝 Contributing

Pull requests are welcome! Feel free to fork the repo and submit improvements or suggestions via PRs.

---

📢 _If you use or extend this project, consider ⭐ starring the repository!_
