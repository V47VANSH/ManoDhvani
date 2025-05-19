# components/log_manager.py

import pandas as pd
import streamlit as st
import os
from datetime import datetime

LOG_PATH = "data/logs.csv"

# Ensure the logs.csv file exists
def initialize_log():
    if not os.path.exists(LOG_PATH):
        df = pd.DataFrame(columns=[
            "Timestamp", "Filename", "Emotion", "Confidence", 
            "Urgency", "Category", "Transcript"
        ])
        df.to_csv(LOG_PATH, index=False)

initialize_log()

def save_to_log(filename, emotion, confidence, urgency, category, transcript):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_entry = pd.DataFrame([{
        "Timestamp": timestamp,
        "Filename": filename,
        "Emotion": emotion,
        "Confidence": round(confidence, 2),
        "Urgency": urgency,
        "Category": category,
        "Transcript": transcript.strip()
    }])

    try:
        df = pd.read_csv(LOG_PATH)
        df = pd.concat([new_entry, df], ignore_index=True)
    except FileNotFoundError:
        df = new_entry

    df.to_csv(LOG_PATH, index=False)

def display_log():
    try:
        df = pd.read_csv(LOG_PATH)
        st.sidebar.dataframe(df.head(10), use_container_width=True)
        with st.sidebar.expander("📥 Download Logs"):
            st.download_button("Download CSV", df.to_csv(index=False), file_name="call_logs.csv")
    except Exception as e:
        st.sidebar.write("No logs found.")