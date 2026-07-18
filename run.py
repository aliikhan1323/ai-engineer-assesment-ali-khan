<<<<<<< HEAD
"""
This script is used to start the FastAPI backend and the Streamlit frontend
"""
#Importing necessary libraries
=======
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
import subprocess
import sys
import time
import signal

<<<<<<< HEAD
#This function is used to start the FastAPI backend and the Streamlit frontend
=======
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
def main():
    # Use the active python interpreter executable to ensure we stay inside the virtual environment
    python_exe = sys.executable
    
    print("🚀 Starting FastAPI backend (uvicorn)...")
    backend_cmd = [python_exe, "-m", "uvicorn", "main:app", "--reload"]
    backend = subprocess.Popen(backend_cmd)
    
    # Wait a few seconds to let FastAPI startup and build/load the vector store
    time.sleep(4)
    
<<<<<<< HEAD
    print("Starting Streamlit frontend...")
=======
    print("🚀 Starting Streamlit frontend...")
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
    frontend_cmd = [python_exe, "-m", "streamlit", "run", "app.py"]
    frontend = subprocess.Popen(frontend_cmd)
    
    print("\n✨ Both applications are running! Press Ctrl+C in this terminal to shut down both.\n")
    
    try:
        while True:
            if backend.poll() is not None:
<<<<<<< HEAD
                print("Backend terminated unexpectedly.")
                break
            if frontend.poll() is not None:
                print("Frontend terminated unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Shutting down applications...")
=======
                print("❌ Backend terminated unexpectedly.")
                break
            if frontend.poll() is not None:
                print("❌ Frontend terminated unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down applications...")
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef
    finally:
        # Gracefully terminate both processes
        backend.terminate()
        frontend.terminate()
<<<<<<< HEAD

        backend.wait()
        frontend.wait()
        print("Both applications have stopped successfully.")
=======
        
        backend.wait()
        frontend.wait()
        print("✅ Both applications have stopped successfully.")
>>>>>>> 2e14aeff5efbb3b06bd3aa03a9da336262d6b7ef

if __name__ == "__main__":
    main()
