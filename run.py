#!/usr/bin/env python3
"""Run the PRD Creator Platform"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    packages = [
        "streamlit",
        "pandas",
        "openpyxl",
        "python-docx",
        "markdown",
        "jinja2",
        "pyyaml"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + packages)

if __name__ == "__main__":
    install_dependencies()
    print("\n" + "="*60)
    print(" 🚀 Starting PRD Creator Platform...")
    print("="*60)
    print("\nOpen your browser to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")

    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"], cwd=os.path.dirname(os.path.abspath(__file__)))