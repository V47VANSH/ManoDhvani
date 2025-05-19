# components/urgency_classifier.py

import re

# Define basic keyword lists (expand as needed)
CATEGORY_KEYWORDS = {
    "Medical": [
        "heart", "attack", "ambulance", "injury", "unconscious", "bleeding", "stroke",
        "seizure", "breathing problem", "chest pain", "collapsed", "not breathing", "dizzy",
        "nauseous", "fever", "infection", "diabetic", "pain", "wound", "hurt", "sick",
        "burn", "cut", "scratched", "bruised", "fracture", "vomiting", "choking",
        "high temperature", "loss of blood", "headache", "pulse", "fainted", "not responsive",
        "low sugar", "asthma", "inhaler", "overdose", "alcohol poisoning", "drunk",
        "swelling", "redness", "discoloration", "medical help", "can't breathe",
        "something wrong", "health issue", "body hurting", "back pain", "ear pain",
        "stomach ache", "collapsed person", "needs doctor", "medic"
    ],
    "Crime": [
        "robbery", "gun", "weapon", "theft", "assault", "burglary", "kidnapping", "hijack",
        "shooting", "stab", "violence", "fight", "criminal", "breaking in", "someone broke in",
        "someone with a knife", "armed", "masked man", "suspicious person", "blackmail",
        "molest", "rape", "murder", "threaten", "smuggling", "snatching", "gang", "goons",
        "violator", "stalking", "following me", "drug dealing", "illegal", "scam", "cheating",
        "cybercrime", "bullying", "extortion", "shoplifting", "vandal", "destruction",
        "harassment", "abduction", "abuser", "suspect", "illegal activity"
    ],
    "Fire": [
        "fire", "burning", "flames", "blaze", "smoke", "sparks", "explosion", "blast",
        "gas leak", "electrical fire", "wildfire", "forest fire", "house on fire", "fire alarm",
        "smoke everywhere", "flaming", "caught fire", "scorch", "ignited", "fire broke out",
        "kitchen fire", "building on fire", "chemical fire", "combustion", "smolder",
        "flaring", "charred", "burnt", "overheated", "short circuit", "power surge",
        "fire in room", "fire accident", "boiler blast"
    ],
    "Domestic Abuse": [
        "abuse", "domestic", "violence", "he's hitting me", "beating", "punch", "slap",
        "choking", "screaming", "yelling", "verbal abuse", "emotional abuse", "physical abuse",
        "she hit me", "threatening", "throwing things", "locked me", "gaslighting",
        "controlling", "toxic", "hurting me", "harassment", "kicking", "mental torture",
        "wife abuse", "husband hitting", "abusive partner", "violence at home",
        "crying in background", "fight in house", "domestic violence", "child abuse",
        "partner hitting", "family abuse", "spouse threatening", "someone hurting",
        "fight at home", "banging", "fear for life"
    ],
    "Accident": [
        "accident", "crash", "car crash", "hit and run", "vehicle", "bike accident",
        "fell down", "ran over", "truck hit", "highway accident", "pile-up", "overturned",
        "road injury", "hurt in accident", "rear-ended", "side collision", "ran into pole",
        "car flipped", "tyre burst", "lost control", "steering failed", "ran off road",
        "impact", "banged into", "airbags deployed", "bus crash", "auto flipped",
        "road mishap", "slipped", "fall", "bridge collapse", "collision", "tram accident",
        "drunk driving", "vehicle fire", "pedestrian hit", "traffic jam due to crash"
    ],
    "Mental Health": [
        "suicidal", "want to die", "depressed", "panic", "anxiety", "can't take it anymore",
        "alone", "overwhelmed", "self harm", "cut myself", "want to kill myself",
        "mental breakdown", "paranoid", "voices", "delusional", "crazy", "unstable",
        "nervous", "stressed", "can't breathe", "crying a lot", "hopeless", "can't cope",
        "losing control", "hearing voices", "hallucinating", "trauma", "triggered",
        "breakdown", "crying uncontrollably", "need therapy", "depression", "burnout",
        "emotional", "want to disappear", "lost", "not feeling okay", "can't sleep",
        "feeling unsafe", "need someone to talk", "help my mind", "freaking out"
    ]
}

URGENCY_KEYWORDS = {
    "High": [
        "help", "urgent", "immediately", "now", "emergency", "critical", "dying",
        "serious", "danger", "need help", "can't wait", "come fast", "need now",
        "hurry", "life or death", "please save", "get here quick", "rushing", "call police",
        "fatal", "life-threatening", "right now", "in big trouble", "massive issue",
        "collapsed", "not moving", "bleeding badly", "severely hurt", "about to die",
        "out of control", "I'm scared", "I fear for life", "fire broke out", "armed attacker"
    ],
    "Medium": [
        "soon", "need assistance", "problem", "issue", "not urgent but serious", "concern",
        "some help", "situation", "help needed", "please come", "respond", "should act",
        "minor injury", "careful", "come when possible", "please send someone",
        "dangerous but stable", "in trouble", "serious matter", "might escalate", "some risk",
        "not severe", "come soon", "moderate concern", "possible threat", "caution needed",
        "waiting for help", "uncertain", "weird situation", "not safe"
    ],
    "Low": [
        "question", "inquiry", "curious", "clarification", "just asking", "mild issue",
        "simple help", "non-emergency", "not urgent", "confused", "seeking advice",
        "routine", "low risk", "not in danger", "feel unsure", "want info", "mild concern",
        "casual", "just reporting", "just letting you know", "general info", "checking in",
        "everything fine", "little help", "no rush", "advice please", "suggest something",
        "don't know what to do", "tiny issue", "not critical"
    ]
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