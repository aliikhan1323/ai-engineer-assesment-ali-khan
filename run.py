import subprocess
import sys
import time
import signal

def main():
    # Use the active python interpreter executable to ensure we stay inside the virtual environment
    python_exe = sys.executable
    
    print("🚀 Starting FastAPI backend (uvicorn)...")
    backend_cmd = [python_exe, "-m", "uvicorn", "main:app", "--reload"]
    backend = subprocess.Popen(backend_cmd)
    
    # Wait a few seconds to let FastAPI startup and build/load the vector store
    time.sleep(4)
    
    print("🚀 Starting Streamlit frontend...")
    frontend_cmd = [python_exe, "-m", "streamlit", "run", "app.py"]
    frontend = subprocess.Popen(frontend_cmd)
    
    print("\n✨ Both applications are running! Press Ctrl+C in this terminal to shut down both.\n")
    
    try:
        while True:
            if backend.poll() is not None:
                print("❌ Backend terminated unexpectedly.")
                break
            if frontend.poll() is not None:
                print("❌ Frontend terminated unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down applications...")
    finally:
        # Gracefully terminate both processes
        backend.terminate()
        frontend.terminate()
        
        backend.wait()
        frontend.wait()
        print("✅ Both applications have stopped successfully.")

if __name__ == "__main__":
    main()
