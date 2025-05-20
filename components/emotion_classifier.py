# components/emotion_classifier.py

import random

# Placeholder emotion classes – must match those your real model will use
EMOTIONS = ["Neutral", "Angry", "Fear", "Distress", "Happy", "Sad"]

def classify_emotion(audio_bytes):
    """
    Placeholder classification logic for UI testing.
    Replace this with actual model inference later.
    
    Returns:
        top_emotion (str): predicted label
        confidence (float): confidence score
        emotion_probs (dict): dictionary of probabilities for each emotion
    """
    # Placeholder deterministic logic for testing
    dummy_probs = {
        "Neutral": 0.1,
        "Angry": 0.25,
        "Fear": 0.15,
        "Distress": 0.3,
        "Happy": 0.1,
        "Sad": 0.1
    }

    top_emotion = max(dummy_probs, key=dummy_probs.get)
    confidence = dummy_probs[top_emotion]

    return top_emotion, confidence, dummy_probs
