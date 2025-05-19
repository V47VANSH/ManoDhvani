# components/emotion_classifier.py

import random

# Dummy emotion classes (replace with your model's output classes)
EMOTIONS = ["Neutral", "Angry", "Fear", "Distress", "Happy", "Sad"]

def classify_emotion(audio_bytes):
    """
    Simulate classification - replace with real model inference.
    Returns (emotion, confidence, emotion_probabilities_dict)
    """
    # Replace this with actual model prediction
    emotion_probs = {e: round(random.uniform(0.05, 0.4), 2) for e in EMOTIONS}
    emotion_probs = {k: v / sum(emotion_probs.values()) for k, v in emotion_probs.items()}

    top_emotion = max(emotion_probs, key=emotion_probs.get)
    confidence = emotion_probs[top_emotion]

    return top_emotion, confidence, emotion_probs