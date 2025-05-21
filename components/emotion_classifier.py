# components/emotion_classifier.py

EMOTIONS = ["Neutral", "Angry", "Fear", "Distress", "Happy", "Sad"]

# Hardcoded test emotion probabilities per audio file
HARDCODED_RESULTS = {
    "test1.wav": {
        "top_emotion": "Neutral",
        "confidence": 0.85,
        "emotion_probs": {
            "Neutral": 0.85,
            "Angry": 0.05,
            "Fear": 0.03,
            "Distress": 0.03,
            "Happy": 0.02,
            "Sad": 0.02,
        },
    },
    "test2.wav": {
        "top_emotion": "Angry",
        "confidence": 0.9,
        "emotion_probs": {
            "Neutral": 0.03,
            "Angry": 0.9,
            "Fear": 0.02,
            "Distress": 0.03,
            "Happy": 0.01,
            "Sad": 0.01,
        },
    },
    "test3.wav": {
        "top_emotion": "Fear",
        "confidence": 0.88,
        "emotion_probs": {
            "Neutral": 0.01,
            "Angry": 0.02,
            "Fear": 0.88,
            "Distress": 0.05,
            "Happy": 0.01,
            "Sad": 0.03,
        },
    },
    "test4.wav": {
        "top_emotion": "Distress",
        "confidence": 0.93,
        "emotion_probs": {
            "Neutral": 0.01,
            "Angry": 0.01,
            "Fear": 0.03,
            "Distress": 0.93,
            "Happy": 0.01,
            "Sad": 0.01,
        },
    },
    "test5.wav": {
        "top_emotion": "Happy",
        "confidence": 0.95,
        "emotion_probs": {
            "Neutral": 0.02,
            "Angry": 0.01,
            "Fear": 0.0,
            "Distress": 0.0,
            "Happy": 0.95,
            "Sad": 0.02,
        },
    },
    "test6.wav": {
        "top_emotion": "Sad",
        "confidence": 0.89,
        "emotion_probs": {
            "Neutral": 0.01,
            "Angry": 0.01,
            "Fear": 0.03,
            "Distress": 0.03,
            "Happy": 0.03,
            "Sad": 0.89,
        },
    },
}

def classify_emotion(audio_bytes, filename=None):
    """
    Return hardcoded prediction based on file name for testing the UI.

    Args:
        audio_bytes (bytes): Audio data (not used here).
        filename (str): Name of the uploaded file, used to simulate prediction.

    Returns:
        top_emotion (str)
        confidence (float)
        emotion_probs (dict)
    """
    if filename in HARDCODED_RESULTS:
        result = HARDCODED_RESULTS[filename]
        return result["top_emotion"], result["confidence"], result["emotion_probs"]
    
    # Fallback if unknown file
    fallback = {
        "top_emotion": "Neutral",
        "confidence": 0.5,
        "emotion_probs": {e: 1/len(EMOTIONS) for e in EMOTIONS}
    }
    return fallback["top_emotion"], fallback["confidence"], fallback["emotion_probs"]