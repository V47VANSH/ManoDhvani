import os
import librosa
import numpy as np
import pandas as pd
import parselmouth
from parselmouth.praat import call

def extract_features(audio_path):
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)
    
    # 1. MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    
    # 2. Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    chroma_std = np.std(chroma, axis=1)
    
    # 3. Spectral Contrast
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = np.mean(contrast, axis=1)
    contrast_std = np.std(contrast, axis=1)
    
    # 4. Tonnetz
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    tonnetz_mean = np.mean(tonnetz, axis=1)
    tonnetz_std = np.std(tonnetz, axis=1)
    
    # 5. Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y=y)
    zcr_mean = np.mean(zcr)
    zcr_std = np.std(zcr)
    
    # 6. Root Mean Square Energy
    rms = librosa.feature.rms(y=y)
    rms_mean = np.mean(rms)
    rms_std = np.std(rms)
    
    # 7. Pitch, Jitter, Shimmer, HNR, Formants
    sound = parselmouth.Sound(audio_path)
    pitch = call(sound, "To Pitch", 0.0, 75, 600)
    point_process = call(sound, "To PointProcess (periodic, cc)", 75, 600)
    
    pitch_mean = call(pitch, "Get mean", 0, 0, "Hertz")
    pitch_min = call(pitch, "Get minimum", 0, 0, "Hertz", "Parabolic")
    pitch_max = call(pitch, "Get maximum", 0, 0, "Hertz", "Parabolic")
    
    jitter_local = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    shimmer_local = call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    
    formant = call(sound, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)
    formant_freqs = [call(formant, "Get value at time", i, 0.5, "Hertz", "Linear") for i in range(1, 4)]  # First 3 formants
    
    # 8. Speech Rate and Pauses
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    if len(onset_times) > 1:
        speech_rate = len(onset_times) / (onset_times[-1] - onset_times[0])  # syllables per second
    else:
        speech_rate = 0
    pauses = np.sum(onset_env < np.mean(onset_env)) / len(onset_env)  # proportion of time with no onset
    
    # Compile all features into a dictionary
    features = {
        'filename': os.path.basename(audio_path),
        'mfcc_mean': mfccs_mean.tolist(),
        'mfcc_std': mfccs_std.tolist(),
        'chroma_mean': chroma_mean.tolist(),
        'chroma_std': chroma_std.tolist(),
        'contrast_mean': contrast_mean.tolist(),
        'contrast_std': contrast_std.tolist(),
        'tonnetz_mean': tonnetz_mean.tolist(),
        'tonnetz_std': tonnetz_std.tolist(),
        'zcr_mean': zcr_mean,
        'zcr_std': zcr_std,
        'rms_mean': rms_mean,
        'rms_std': rms_std,
        'pitch_mean': pitch_mean,
        'pitch_min': pitch_min,
        'pitch_max': pitch_max,
        'jitter': jitter_local,
        'shimmer': shimmer_local,
        'hnr': hnr,
        'formants': formant_freqs,
        'speech_rate': speech_rate,
        'pauses': pauses
    }
    
    return features

def extract_features_from_directory(directory):
    all_features = []
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            audio_path = os.path.join(directory, filename)
            features = extract_features(audio_path)
            all_features.append(features)
    
    return pd.DataFrame(all_features)

# Example usage
audio_directory = 'Audio_files_1'
features_df = extract_features_from_directory(audio_directory)
features_df.to_csv('audio_features.csv', index=False)
