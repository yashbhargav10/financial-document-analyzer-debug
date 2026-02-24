import requests
import time
import json

URL = "http://127.0.0.1:8000"

print("===========================================")
print(" 1. Testing Health Check (GET /) ")
print("===========================================")
try:
    health = requests.get(f"{URL}/")
    print(f"Status: {health.status_code}")
    print(f"Response: {health.json()}")
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to the API. Make sure 'py main.py' is running!")
    exit(1)

print("\n===========================================")
print(" 2. Starting Analysis Task (POST /analyze) ")
print("===========================================")
print("Sending request with a dummy PDF file...")

# We'll create a quick dummy PDF data source if the sample.pdf doesn't exist
try:
    with open("data/sample.pdf", "rb") as f:
        file_data = f.read()
except FileNotFoundError:
    print("Warning: data/sample.pdf not found. We will send a dummy text file as a mock PDF.")
    file_data = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    
response = requests.post(
    f"{URL}/analyze", 
    files={"file": ("dummy_report.pdf", file_data, "application/pdf")},
    data={"query": "Please provide a brief investment summary and any risks mentioned."}
)

if response.status_code != 200:
    print(f"Failed to start task. Status: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()
print("Success! Task Queued.")
print(json.dumps(data, indent=2))

task_id = data["task_id"]

print("\n===========================================")
print(" 3. Polling for Status (GET /status/{task_id}) ")
print("===========================================")
print(f"Waiting for CrewAI agents to finish task: {task_id}")
print("This may take 30-60 seconds depending on the API calls...")

while True:
    status_response = requests.get(f"{URL}/status/{task_id}")
    status_data = status_response.json()
    
    status = status_data["status"]
    
    if status == "pending":
        print(f"Status: {status}... still working. Sleeping for 5 seconds.")
        time.sleep(5)
    elif status == "completed":
        print("\n\n" + "="*50)
        print(" 🎉 ANALYSIS COMPLETED 🎉 ")
        print("="*50)
        print("\n" + status_data["result"])
        break
    elif status == "failed":
        print("\n\n" + "="*50)
        print(" ❌ ANALYSIS FAILED ❌ ")
        print("="*50)
        print("\nError Details:")
        print(status_data["result"])
        break
    else:
        print(f"Unknown status: {status}")
        break 
