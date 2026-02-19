
import urllib.request
import json
import ssl

# Supabase Config
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
BASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co/rest/v1/question_bank"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def verify_data():
    print("Verifying Supabase Data...")
    context = ssl._create_unverified_context()
    
    # Check 1: Total Count
    try:
        url = f"{BASE_URL}?select=count"
        req = urllib.request.Request(url, headers=HEADERS)
        # Range header is needed for count usually, but let's try basic select first
        url = f"{BASE_URL}?select=*&limit=1"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=context) as response:
            print(f"Connection check: {response.status}")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # Check 2: Search for 'Onion' (Case Study Identifier)
    try:
        print("\nSearching for 'Onion'...")
        url = f"{BASE_URL}?question_text=ilike.*Onion*"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=context) as response:
            data = json.loads(response.read().decode())
            print(f"Found {len(data)} questions containing 'Onion'.")
            if len(data) > 0:
                text = data[0].get('question_text', '')
                print(f"Sample text: {text}")
                if "[Image:" in text:
                    print("SUCCESS: Image marker found in text.")
                else:
                    print("FAILURE: Text found but NO image marker.")
    except Exception as e:
        print(f"Search failed: {e}")
    
    # Check 3: Search for '[Image:' explicitly again
    try:
        print("\nSearching for '[Image:' marker...")
        # URL encode [ and ] -> %5B and %5D
        url = f"{BASE_URL}?question_text=ilike.*%5BImage:*&limit=5"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=context) as response:
            data = json.loads(response.read().decode())
            print(f"Found {len(data)} questions with marker in DB.")
    except Exception as e:
        print(f"Marker search failed: {e}")

if __name__ == "__main__":
    verify_data()
