import os
import streamlit as st
import subprocess
import sys
import threading
import time

st.set_page_config(page_title="📧 Gmail Automation Dashboard", page_icon="📩")

st.title("📧 Gmail Automation Dashboard")

if 'process' not in st.session_state:
    st.session_state.process = None

def stream_logs(process):
    """Continuously read logs from the background process."""
    with open('temp_logs.txt', 'a', encoding='utf-8') as f:
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # Print to terminal
            f.write(line)
            f.flush()
            # Update progress based on events using file
            if 'EVENT:FETCHING_EMAILS:START' in line:
                update_progress_status(0, "🏁 Fetching emails...")
            elif 'EVENT:FETCHING_EMAILS:COMPLETE' in line:
                update_progress_status(25, "📨 Processing emails...")
            elif 'EVENT:LLM_PARSE:COMPLETE' in line:
                update_progress_status(50, "🤖 Parsing and checking database...")
            elif 'EVENT:SHEET_UPDATE:COMPLETE' in line:
                update_progress_status(75, "📊 Updating Google Sheet...")
            elif 'EVENT:ACK_EMAIL:COMPLETE' in line:
                update_progress_status(100, "📬 Sending acknowledgment...")
            elif 'RESET_CYCLE' in line:
                update_progress_status(0, "Waiting for new emails...")
    process.stdout.close()

def update_progress_status(progress, status_text):
    """Update progress and status in file."""
    with open('temp_progress.txt', 'w', encoding='utf-8') as f:
        f.write(f"{progress}\n{status_text}")

def start_automation():
    if st.session_state.process is None or st.session_state.process.poll() is not None:
        if os.path.exists('temp_logs.txt'):
            os.remove('temp_logs.txt')
        if os.path.exists('temp_progress.txt'):
            os.remove('temp_progress.txt')
        update_progress_status(0, "Waiting for new emails...")
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'  # Force unbuffered output
        st.session_state.process = subprocess.Popen(
            [sys.executable, 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env
        )
        threading.Thread(target=stream_logs, args=(st.session_state.process,), daemon=True).start()
        st.success("🚀 Automation started!")



def stop_automation():
    if st.session_state.process and st.session_state.process.poll() is None:
        st.session_state.process.kill()
        st.session_state.process.wait()
        st.success("🛑 Automation stopped.")
    st.session_state.process = None

# Button to start automation
if st.button("🚀 Start Automation"):
    start_automation()

# Stop button
if st.button("🛑 Stop Automation"):
    stop_automation()

# Status
status = "🟢 Running" if st.session_state.process and st.session_state.process.poll() is None else "🔴 Stopped"
st.markdown(f"**Status:** {status}")

# Progress
progress = 0
status_text = "Waiting for new emails..."
if os.path.exists('temp_progress.txt'):
    with open('temp_progress.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if content:
            parts = content.split('\n', 1)
            if len(parts) == 2:
                progress = int(parts[0])
                status_text = parts[1]

st.progress(progress / 100)
st.caption(f"{progress}% - {status_text}")

# Auto-refresh logs every 1 second
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1000, key="log_refresh")

# Read logs from file and reverse order (newest on top)
logs = ""
if os.path.exists('temp_logs.txt'):
    with open('temp_logs.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        reversed_lines = lines[::-1]
        logs = '\n'.join(reversed_lines)

st.text_area("Logs", logs, height=400)
