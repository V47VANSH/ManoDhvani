from keywords.keywords import *

def calculate_urgency(text):
    text = text.lower()
    score = 0
    max_score = 0

    for word in high_urgency_keywords_en + high_urgency_keywords_hi:
        if word in text:
            score += 3
            max_score += 3
    for word in medium_urgency_keywords_en + medium_urgency_keywords_hi:
        if word in text:
            score += 2
            max_score += 3
    for word in low_urgency_keywords_en + low_urgency_keywords_hi:
        if word in text:
            score += 1
            max_score += 3

    if max_score == 0:
        return 0, "Not Urgent"

    percentage = (score / max_score) * 100

    if percentage >= 66:
        urgency_label = "High Urgency"
    elif percentage >= 33:
        urgency_label = "Medium Urgency"
    else:
        urgency_label = "Low Urgency"

    return percentage, urgency_label

