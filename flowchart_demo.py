"""
RFQ Automation Flowchart Dashboard - WORKING VERSION
Beautiful visual flowchart that works with your existing main.py
"""
import os
import streamlit as st
import subprocess
import sys
import threading
import time
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="🚀 RFQ Automation Dashboard", 
    page_icon="📧",
    layout="wide"
)

# Custom CSS for beautiful flowchart
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .step-box {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        min-height: 200px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .step-pending {
        opacity: 0.6;
        border: 3px dashed #ccc;
    }
    
    .step-processing {
        border: 3px solid #3498db;
        animation: pulse 2s infinite;
        transform: scale(1.02);
    }
    
    .step-completed {
        border: 3px solid #2ecc71;
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 10px 30px rgba(52, 152, 219, 0.3); }
        50% { box-shadow: 0 10px 40px rgba(52, 152, 219, 0.6); }
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'process' not in st.session_state:
    st.session_state.process = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'step_logs' not in st.session_state:
    st.session_state.step_logs = {1: [], 2: [], 3: [], 4: []}
if 'step_status' not in st.session_state:
    st.session_state.step_status = {1: 'pending', 2: 'pending', 3: 'pending', 4: 'pending'}

# Auto-refresh every 1 second
st_autorefresh(interval=1000, key="refresh")

def stream_logs(process):
    """Read logs from the background process and write to file."""
    for line in iter(process.stdout.readline, ''):
        print(line, end='')  # Print to terminal for debugging
        
        # Write to temp file for persistence
        with open('temp_automation_log.txt', 'a', encoding='utf-8') as f:
            f.write(line)
            f.flush()
            
    process.stdout.close()

def update_step_status_from_log():
    """Read log file and update step status (called from main thread)."""
    if not os.path.exists('temp_automation_log.txt'):
        return
    
    try:
        with open('temp_automation_log.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Process lines in order to determine current state
        for line in lines:
            if 'EVENT:FETCHING_EMAILS:START' in line:
                st.session_state.current_step = 1
                st.session_state.step_status[1] = 'processing'
                if "📧 Checking for new RFQ emails..." not in st.session_state.step_logs[1]:
                    st.session_state.step_logs[1].append("📧 Checking for new RFQ emails...")
                
            elif 'EVENT:FETCHING_EMAILS:COMPLETE' in line:
                st.session_state.step_status[1] = 'completed'
                if "✅ Email fetched successfully" not in st.session_state.step_logs[1]:
                    st.session_state.step_logs[1].append("✅ Email fetched successfully")
                
            elif '[ALERT]' in line and 'new inquiry' in line:
                log_text = line.strip()
                if log_text not in st.session_state.step_logs[1]:
                    st.session_state.step_logs[1].append(log_text)
                
            elif 'EVENT:LLM_PARSE:COMPLETE' in line:
                st.session_state.current_step = 2
                st.session_state.step_status[2] = 'processing'
                if "🔍 Checking customer database..." not in st.session_state.step_logs[2]:
                    st.session_state.step_logs[2].append("🔍 Checking customer database...")
                
            elif '[USER] New potential client added' in line:
                if "🆕 New client detected and added" not in st.session_state.step_logs[2]:
                    st.session_state.step_logs[2].append("🆕 New client detected and added")
                st.session_state.step_status[2] = 'completed'
                
            elif '[USER] Existing client updated' in line:
                if "✅ Existing client found" not in st.session_state.step_logs[2]:
                    st.session_state.step_logs[2].append("✅ Existing client found")
                st.session_state.step_status[2] = 'completed'
                
            elif 'EVENT:SHEET_UPDATE:COMPLETE' in line:
                st.session_state.current_step = 3
                st.session_state.step_status[3] = 'processing'
                if "📊 Updating Google Spreadsheet..." not in st.session_state.step_logs[3]:
                    st.session_state.step_logs[3].append("📊 Updating Google Spreadsheet...")
                
            elif '[BAR] Inquiry logged to tracking dashboard' in line:
                if "✅ Spreadsheet updated successfully" not in st.session_state.step_logs[3]:
                    st.session_state.step_logs[3].append("✅ Spreadsheet updated successfully")
                st.session_state.step_status[3] = 'completed'
                # Start Step 4 immediately after Step 3 completes
                st.session_state.current_step = 4
                st.session_state.step_status[4] = 'processing'
                if "✉️ Sending acknowledgment email..." not in st.session_state.step_logs[4]:
                    st.session_state.step_logs[4].append("✉️ Sending acknowledgment email...")
                
            elif '[OK] Automatic reply sent' in line:
                if "✅ Acknowledgment sent to customer" not in st.session_state.step_logs[4]:
                    st.session_state.step_logs[4].append("✅ Acknowledgment sent to customer")
                st.session_state.step_status[4] = 'completed'
                
            elif 'EVENT:ACK_EMAIL:COMPLETE' in line:
                # Ensure Step 4 is marked as completed
                st.session_state.step_status[4] = 'completed'
                
            elif 'RESET_CYCLE' in line:
                # Mark for reset (will happen on next refresh)
                pass
                
    except Exception as e:
        print(f"Error reading log: {e}")

def start_automation():
    """Start the automation process."""
    if st.session_state.process is None or st.session_state.process.poll() is not None:
        # Clear previous logs
        if os.path.exists('temp_automation_log.txt'):
            os.remove('temp_automation_log.txt')
        
        # Reset step status
        for i in range(1, 5):
            st.session_state.step_status[i] = 'pending'
            st.session_state.step_logs[i] = []
        st.session_state.current_step = 0
        
        # Start main.py process
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        
        st.session_state.process = subprocess.Popen(
            [sys.executable, 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Start log streaming thread
        threading.Thread(target=stream_logs, args=(st.session_state.process,), daemon=True).start()
        return True
    return False

def stop_automation():
    """Stop the automation process."""
    if st.session_state.process and st.session_state.process.poll() is None:
        st.session_state.process.kill()
        st.session_state.process.wait()
    st.session_state.process = None
    
    # Reset all steps
    for i in range(1, 5):
        st.session_state.step_status[i] = 'pending'
        st.session_state.step_logs[i] = []
    st.session_state.current_step = 0

# Update step status from log file (runs in main thread - safe!)
update_step_status_from_log()

# Title
st.markdown("""
<div style='text-align: center; color: white; padding: 20px;'>
    <h1 style='font-size: 3rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        🚀 RFQ Automation Dashboard
    </h1>
    <p style='font-size: 1.2rem; opacity: 0.9;'>Real-time Workflow Visualization</p>
</div>
""", unsafe_allow_html=True)

# Control Panel
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    if st.button("🚀 Start Automation", type="primary", use_container_width=True):
        if start_automation():
            st.success("✅ Automation started!")
            time.sleep(1)
            st.rerun()

with col2:
    if st.button("🛑 Stop Automation", use_container_width=True):
        stop_automation()
        st.warning("🛑 Automation stopped")
        time.sleep(1)
        st.rerun()

with col3:
    is_running = st.session_state.process and st.session_state.process.poll() is None
    status = "🟢 Running" if is_running else "🔴 Stopped"
    st.markdown(f"<h3 style='text-align: center; color: white;'>{status}</h3>", unsafe_allow_html=True)

# Metrics Row
st.markdown("<br>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric-card">
        <h2 style='color: #667eea; margin: 0;'>0</h2>
        <p style='margin: 5px 0 0 0; color: #666;'>RFQs Processed</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    completed = sum(1 for s in st.session_state.step_status.values() if s == 'completed')
    st.markdown(f"""
    <div class="metric-card">
        <h2 style='color: #667eea; margin: 0;'>{completed}/4</h2>
        <p style='margin: 5px 0 0 0; color: #666;'>Steps Completed</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    processing = sum(1 for s in st.session_state.step_status.values() if s == 'processing')
    st.markdown(f"""
    <div class="metric-card">
        <h2 style='color: #667eea; margin: 0;'>{processing}</h2>
        <p style='margin: 5px 0 0 0; color: #666;'>In Progress</p>
    </div>
    """, unsafe_allow_html=True)

with m4:
    pending = sum(1 for s in st.session_state.step_status.values() if s == 'pending')
    st.markdown(f"""
    <div class="metric-card">
        <h2 style='color: #667eea; margin: 0;'>{pending}</h2>
        <p style='margin: 5px 0 0 0; color: #666;'>Pending</p>
    </div>
    """, unsafe_allow_html=True)

# Flowchart Steps
st.markdown("<br><h2 style='text-align: center; color: white;'>Workflow Steps</h2>", unsafe_allow_html=True)

steps = [
    (1, "📧 Processing New RFQ Email", "Fetching and analyzing incoming RFQ emails"),
    (2, "🗄️ Checking Customer Database", "Verifying if customer exists in database"),
    (3, "📊 Updating Google Spreadsheet", "Logging RFQ data to tracking sheet"),
    (4, "✉️ Sending Acknowledgment", "Sending automatic reply to customer")
]

cols = st.columns(4)

for idx, (step_num, title, description) in enumerate(steps):
    with cols[idx]:
        status = st.session_state.step_status[step_num]
        
        # Determine icon based on status
        if status == 'completed':
            icon = "✅"
            box_class = "step-completed"
        elif status == 'processing':
            icon = "⚙️"
            box_class = "step-processing"
        else:
            icon = "⏳"
            box_class = "step-pending"
        
        # Build logs HTML
        logs_html = ""
        if st.session_state.step_logs[step_num]:
            logs_html = "<div style='margin-top: 10px; font-size: 0.85rem;'>"
            for log in st.session_state.step_logs[step_num][-3:]:  # Show last 3 logs
                logs_html += f"<div style='padding: 2px 0; color: #555;'>{log}</div>"
            logs_html += "</div>"
        
        st.markdown(f"""
        <div class="step-box {box_class}">
            <div style='text-align: center; font-size: 2rem;'>{icon}</div>
            <h4 style='text-align: center; margin: 10px 0;'>Step {step_num}</h4>
            <h5 style='margin: 5px 0; color: #333;'>{title}</h5>
            <p style='font-size: 0.9rem; color: #666; margin: 5px 0;'>{description}</p>
            {logs_html}
        </div>
        """, unsafe_allow_html=True)

# Process Output Section
st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: white;'>📟 Live Process Output</h3>", unsafe_allow_html=True)

# Show last lines from log file
if os.path.exists('temp_automation_log.txt'):
    with open('temp_automation_log.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        last_lines = lines[-20:] if len(lines) > 20 else lines
        output = ''.join(last_lines)
        st.code(output, language="log")
else:
    st.info("No output yet. Click 'Start Automation' to begin.")

# Debug info
with st.expander("🐛 Debug Information"):
    st.write("**Process Status:**")
    if st.session_state.process:
        st.code(f"PID: {st.session_state.process.pid if st.session_state.process.poll() is None else 'Not running'}")
        st.code(f"Return Code: {st.session_state.process.poll()}")
    else:
        st.code("No process started")
    
    st.write("**Current Step:**", st.session_state.current_step)
    st.write("**Step Status:**", st.session_state.step_status)
