import os
import sys
import webbrowser
import time
import uvicorn

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

def main():
    print("============================================================")
    print("🧠 Starting AIOps Copilot — Intelligent Incident Platform...")
    print("============================================================")

    # Path to frontend dashboard
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend", "index.html"))
    print(f"📊 Dashboard available at: file:///{frontend_path.replace('\\', '/')}")
    
    # Open dashboard in web browser after 1.5 seconds
    try:
        webbrowser.open(f"file:///{frontend_path.replace('\\', '/')}")
    except Exception as e:
        print(f"Notice: Could not automatically open browser: {e}")

    print("🚀 API Server starting on http://127.0.0.1:8000...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
