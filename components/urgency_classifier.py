# components/urgency_classifier.py

import re

# Define basic keyword lists (expand as needed)
CATEGORY_KEYWORDS = {
    "Medical": ["heart", "ambulance", "injury", "unconscious", "bleeding", "stroke"],
    "Crime": ["robbery", "gun", "weapon", "theft", "assault", "fight", "burglary"],
    "Fire": ["fire", "burn", "smoke", "explosion", "blaze"],
    "Domestic Abuse": ["abuse", "violence", "husband", "beating", "threaten", "screaming"],
    "Accident": ["crash", "accident", "hit", "road", "car", "bike"],
    "Mental Health": ["suicide", "depressed", "mental", "panic", "anxiety", "help myself"],
}

URGENCY_KEYWORDS = {
    "High": ["help", "immediately", "urgent", "now", "asap", "emergency"],
    "Medium": ["soon", "need assistance", "problem", "situation", "support"],
    "Low": ["question", "confused", "advice", "suggest", "inquire"],
}

def classify_urgency(transcript, emotion):
    transcript_lower = transcript.lower()

    # Default values
    urgency = "Medium"
    category = "General"

    # Determine category
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in transcript_lower for kw in keywords):
            category = cat
            break

    # Determine urgency
    for level, keywords in URGENCY_KEYWORDS.items():
        if any(kw in transcript_lower for kw in keywords):
            urgency = level
            break

    # Optional: boost urgency if emotion is aggressive/distressed
    if emotion.lower() in ["angry", "distress", "fear"] and urgency != "High":
        urgency = "High"

    return urgency, category