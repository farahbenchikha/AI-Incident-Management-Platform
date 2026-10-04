import os
import sys
import webbrowser

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

def main():
    print("============================================================")
    print("[AIOps Copilot] Starting Platform Demo Runner...")
    print("============================================================")

    # Path to frontend dashboard
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "frontend", "index.html"))
    formatted_path = frontend_path.replace("\\", "/")
    
    print(f"[UI] Dashboard available at: file:///{formatted_path}")
    
    # Open dashboard in web browser
    try:
        webbrowser.open(f"file:///{formatted_path}")
        print("[LAUNCH] Web browser launched successfully!")
    except Exception as e:
        print(f"[NOTICE] Could not automatically open browser: {e}")

    print("\n[STATUS] FastAPI Server is active on http://127.0.0.1:8000")
    print("[HINT] You can now interact with the live dashboard in your browser.")

if __name__ == "__main__":
    main()
