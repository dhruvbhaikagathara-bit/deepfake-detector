import requests
import time

url = 'http://127.0.0.1:5000/api/health'

print("🧪 Testing Rate Limiting...")
print("Sending 25 requests quickly...\n")

for i in range(25):
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"✅ Request {i+1}: Success")
    elif response.status_code == 429:
        print(f"⛔ Request {i+1}: Rate Limited!")
        print(f"   Message: {response.json()['message']}")
        break
    
    time.sleep(0.1)  # Small delay between requests

print("\n✅ Rate limiting is working!")