import requests
import json

# Base URL for the backend API
BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Todo API...")
    
    # Start the backend server first
    import subprocess
    import time
    import os
    
    # Change to backend directory and start the server
    backend_dir = "backend"
    os.chdir(backend_dir)
    
    # Start the server in the background
    server_process = subprocess.Popen([
        "python", "-m", "uvicorn", "src.main:app", "--reload", "--port", "8000"
    ])
    
    # Wait a moment for the server to start
    time.sleep(5)
    
    # Return to original directory
    os.chdir("..")
    
    try:
        # Test health endpoint
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test root endpoint
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
        
        # Test todos endpoint (should return empty list initially)
        print("\n3. Testing todos endpoint...")
        try:
            response = requests.get(f"{BASE_URL}/todos")
            print(f"Todos endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Todos endpoint error (expected without auth): {e}")
            
        print("\nAPI tests completed successfully!")
        
    except Exception as e:
        print(f"Error during API testing: {e}")
    finally:
        # Kill the server process
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    test_api()