import os
import librosa
import numpy as np
import pandas as pd
import parselmouth
from parselmouth.praat import call
import soundfile as sf
from scipy.fft import fft
import opensmile
from opensmile import FeatureSet, FeatureLevel


def extract_features_opsm(y, sr) -> pd.DataFrame:
    # Create an instance of the Smile class with a standard feature set
    # ComParE_2016 is a popular set for emotion recognition
    smile = opensmile.Smile(
        feature_set=FeatureSet.eGeMAPSv02,
        feature_level=FeatureLevel.Functionals
    )

    # Extract features from the audio file
    features = smile.process_signal(y, sampling_rate=sr)
    return features


# This function extracts various audio features from .wav files in a specified directory.
# It includes features like MFCCs, Chroma, Spectral Contrast, Tonnetz, Zero Crossing Rate,
def extract_features(y, sr):
    # Load audio file
    # y, sr = librosa.load(audio_path, sr=None)
    # y, sr = sf.read(audio_path, always_2d=False)  # y is a numpy array, dtype matches file
    
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
    sound = parselmouth.Sound(y, sr)
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
        # 'filename': os.path.basename(audio_path),
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

def complex_fft(y, sr):
    # Compute the complex FFT
    X_complex = fft(y)
    # Retain real and imaginary parts separately
    X_real = np.real(X_complex)
    X_imag = np.imag(X_complex)
    return X_real, X_imag


def compute_sta_lta(y, sr):

    sta_window = int(0.025 * sr)  # 50 ms
    lta_window = int(0.25 * sr)   # 500 ms
    """
    Compute STA/LTA ratio for a 1D signal.
    
    Parameters:
    - y: 1D numpy array (audio signal)
    - sta_window: short-term window length (in samples)
    - lta_window: long-term window length (in samples)
    
    Returns:
    - sta_lta: STA/LTA ratio (1D numpy array)
    """
    y = np.abs(y)  # Rectified signal (energy-based)
    
    sta = np.convolve(y, np.ones(sta_window)/sta_window, mode='same')
    lta = np.convolve(y, np.ones(lta_window)/lta_window, mode='same')
    
    # Avoid division by zero
    lta[lta == 0] = 1e-10
    
    sta_lta = sta / lta
    # N = len(y)

    sta_lta = (sta_lta - sta_lta.min()) / (sta_lta.max() - sta_lta.min() + 1e-9)
    # t = np.arange(N) / sr
    sta_lta_2d = sta_lta[np.newaxis, :]

    return sta_lta_2d



def data_preprocessing(y, sr):
    features_opsm = extract_features_opsm(y, sr)
    features = extract_features(y, sr)
    X_real, X_imag = complex_fft(y, sr)
    sta_lta = compute_sta_lta(y, sr)
    features_opsm = features_opsm.to_numpy()
    features = features.to_numpy()
    stacked = np.stack((features_opsm, features, X_real, X_imag, sta_lta), axis=0)
    return stacked
    




# def extract_features_from_directory(directory):
#     all_features = []
#     for filename in os.listdir(directory):
#         if filename.endswith('.wav'):
#             audio_path = os.path.join(directory, filename)
#             y , sr = sf.read(audio_path, always_2d=False)
#             features_opsm = extract_features_opsm(y, sr)
#             features = extract_features(y, sr)
#             X_real, X_imag = complex_fft(y, sr)
#             sta_lta = compute_sta_lta(y, sr)
#             # Add filename as a column for identification
#             # features['filename'] = os.path.basename(audio_path)
#             # all_features.append(features)
    
#     # Concatenate all DataFrames in the list
#     # if all_features:
#     #     return pd.concat(all_features, ignore_index=True)
#     # else:
#     return pd.DataFrame(all_features)  # Return empty DataFrame if no files were processed

# # # Example usage
# # audio_directory = 'Audio files'
# # features_df = extract_features_from_directory(audio_directory)
# # features_df.to_csv('audio_ggaas.csv', index=False)
