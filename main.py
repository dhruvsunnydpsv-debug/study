import os
import requests
import time
from supabase import create_client

# 1. SETUP & DEBUG
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
SERPER_KEY = os.environ.get("SERPER_KEY")

print(f"--- DEBUG INFO ---")
print(f"URL exists: {bool(URL)}")
print(f"KEY exists: {bool(KEY)}")
print(f"SERPER exists: {bool(SERPER_KEY)}")

if not URL or not KEY or not SERPER_KEY:
    raise ValueError("CRITICAL ERROR: One of your Secrets is missing in GitHub Settings!")

supabase = create_client(URL, KEY)

# 2. TEST CONNECTION FIRST
print("--- TESTING DATABASE CONNECTION ---")
try:
    test_data = {"file_name": "TEST_ENTRY", "subject": "Debug", "file_url": "http://test.com"}
    response = supabase.table("source_papers").upsert(test_data, on_conflict="file_url").execute()
    print("✅ Connection Successful! Test row inserted.")
except Exception as e:
    print(f"❌ DATABASE ERROR: {e}")
    raise e # Crash the script so we know it failed

# 3. THE HUNT
syllabus = {"Maths": ["Polynomials"]} # Checking just ONE chapter first to be fast

def hunt():
    print("--- STARTING HUNT ---")
    query = "filetype:pdf class 9 maths polynomials question paper rationalised 2025"
    
    headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}
    response = requests.post("https://google.serper.dev/search", json={"q": query, "num": 10}, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ SERPER API ERROR: {response.text}")
        return

    results = response.json().get('organic', [])
    print(f"🔎 Found {len(results)} links for Polynomials")

    for item in results:
        print(f"   -> Saving: {item.get('title')}")
        data = {
            "file_name": item.get('title'),
            "file_url": item.get('link'),
            "subject": "Maths",
            "chapter": "Polynomials"
        }
        try:
            supabase.table("source_papers").upsert(data, on_conflict="file_url").execute()
        except Exception as e:
            print(f"   ❌ INSERT FAILED: {e}")

if __name__ == "__main__":
    hunt()
