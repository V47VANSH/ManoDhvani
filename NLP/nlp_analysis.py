from keywords.keywords import *

def calculate_urgency_percentage(text):
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
        label = "High Urgency"
    elif percentage >= 33:
        label = "Medium Urgency"
    else:
        label = "Low Urgency"

    return percentage, label

