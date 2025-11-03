"""
Simple launcher for the flowchart dashboard
"""
import subprocess
import sys

print("\n" + "="*50)
print("  🚀 RFQ AUTOMATION FLOWCHART DASHBOARD")
print("="*50 + "\n")

print("Starting dashboard...")
subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'flowchart_demo.py'])
