# components/log_manager.py

import pandas as pd
import streamlit as st
import os
from datetime import datetime

LOG_PATH = "data/logs.csv"

# Ensure the logs.csv file exists with headers
def initialize_log():
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0:
        df = pd.DataFrame(columns=[
            "Timestamp", "Filename", "Emotion", "Confidence", 
            "Urgency_Level", "Urgency_Category", "Urgency_Percentage" "Transcript"
        ])
        df.to_csv(LOG_PATH, index=False)

initialize_log()

def save_to_log(filename, emotion, confidence, urgency_label, category, percentage, transcripted_text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_entry = pd.DataFrame([{
        "Timestamp": timestamp,
        "Filename": filename,
        "Emotion": emotion,
        "Confidence": round(confidence, 2),
        "Urgency_Level": urgency_label,
        "Urgency_Category": category,
        "Urgency_Percentage": round(percentage, 2),
        "Transcript": transcripted_text.strip()
    }])

    try:
        if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 0:
            df = pd.read_csv(LOG_PATH)
            df = pd.concat([new_entry, df], ignore_index=True)
        else:
            df = new_entry
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = new_entry

    df.to_csv(LOG_PATH, index=False)

def display_log():
    try:
        if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 0:
            df = pd.read_csv(LOG_PATH)
            st.sidebar.dataframe(df.head(10), use_container_width=True)
            with st.sidebar.expander("📥 Download Logs"):
                st.download_button("Download CSV", df.to_csv(index=False), file_name="call_logs.csv")
        else:
            st.sidebar.write("No logs found.")
    except Exception as e:
        st.sidebar.write("Error loading logs.")
        st.sidebar.text(str(e))

