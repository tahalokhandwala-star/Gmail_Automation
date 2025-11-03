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
    process.stdout.close()

def start_automation():
    if st.session_state.process is None or st.session_state.process.poll() is not None:
        if os.path.exists('temp_logs.txt'):
            os.remove('temp_logs.txt')
        if os.path.exists('temp_status.txt'):
            os.remove('temp_status.txt')
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
progress_value = 0
progress_text = "Waiting for new emails"
if os.path.exists('temp_status.txt'):
    with open('temp_status.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if content:
            parts = content.split('\n', 1)
            if len(parts) == 2:
                progress_value = int(parts[0])
                progress_text = parts[1]

st.progress(progress_value / 100)
st.caption(progress_text)

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
