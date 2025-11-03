import os
import subprocess
import threading
import sys
import time
from nicegui import ui

# Shared logs outside NiceGUI context
shared_logs = []

def stream_logs(process):
    """Continuously read logs from the background process."""
    for line in iter(process.stdout.readline, ''):
        shared_logs.append(line)
    process.stdout.close()

process = None
logs = ""

def start_automation():
    """Start main.py as background process and stream logs."""
    global process, logs, shared_logs
    if not os.path.exists('token.pickle'):
        ui.notify("Authentication required: Please run 'python main.py' in a terminal first to authenticate with Google, then start from the UI.", type="error")
        return
    if process is None or process.poll() is not None:
        logs = ""
        shared_logs.clear()
        process = subprocess.Popen(
            [sys.executable, 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        threading.Thread(target=stream_logs, args=(process,), daemon=True).start()
        ui.notify("🚀 Automation started successfully!")

def stop_automation():
    """Stop background process."""
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
        ui.notify("🛑 Automation stopped.")
    process = None

@ui.page('/')
def main():
    ui.page_title("📧 Gmail Automation Dashboard")
    ui.label("📧 Gmail Automation Dashboard").classes('text-xl')
    ui.label("Start the Gmail automation process in the background and monitor logs in real time.").classes('text-lg')

    # Button to start automation
    ui.button("🚀 Start Automation", on_click=start_automation)

    # Stop button
    stop_btn = ui.button("🛑 Stop Automation", on_click=stop_automation)

    # Status label
    status_label = ui.label("Status: 🔴 Stopped")

    # Progress indicator
    progress = ui.linear_progress(0, show_value=False)
    progress.visible = False

    # Logs text area
    log_area = ui.textarea("Logs", value=logs).classes('w-full h-96')

    def update_ui():
        global logs, shared_logs
        if process and process.poll() is None:
            progress.visible = True
            progress.value = (time.time() % 100) / 100 * 100  # Arbitrary progress
            status_label.text = "Status: 🟢 Running"
            stop_btn.visible = True
        else:
            progress.visible = False
            status_label.text = "Status: 🔴 Stopped"
            stop_btn.visible = False

        if shared_logs:
            logs += ''.join(shared_logs)
            log_area.value = logs
            shared_logs.clear()

    # Update every 2 seconds
    ui.timer(2.0, update_ui)

ui.run(reload=False, port=8501)
