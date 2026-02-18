import requests
import time
from supabase import create_client

# --- FORCE-FED CREDENTIALS (NO SECRETS) ---
SUPABASE_URL = "https://wfegoasrtbhpursgcvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
SERPER_KEY = "08f33a092d4657bd7ef7da25237b2d40703b9698"

print("--- 1. CONNECTING TO DATABASE ---")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# TEST INSERT - If this fails, the script CRASHES immediately
test_payload = {"file_name": "GITHUB_TEST_ROW", "file_url": "http://github-test.com", "subject": "TEST", "chapter": "TEST"}
print("--- 2. ATTEMPTING TEST INSERT ---")
# This line will throw a CRITICAL ERROR if RLS is blocking it
supabase.table("source_papers").upsert(test_payload, on_conflict="file_url").execute()
print("✅ SUCCESS: Database is writable!")

def hunt():
    print("--- 3. STARTING SEARCH ---")
    query = "filetype:pdf class 9 maths polynomials question paper 2025"
    headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}
    
    response = requests.post("https://google.serper.dev/search", json={"q": query, "num": 5}, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"❌ API FAILED: {response.text}")

    results = response.json().get('organic', [])
    print(f"🔎 Found {len(results)} links")

    if not results:
        raise Exception("❌ SEARCH FAILED: No results found!")

    for item in results:
        print(f"   -> Saving: {item.get('title')}")
        data = {
            "file_name": item.get('title'),
            "file_url": item.get('link'),
            "subject": "Maths",
            "chapter": "Polynomials"
        }
        # If this fails, the script CRASHES
        supabase.table("source_papers").upsert(data, on_conflict="file_url").execute()

if __name__ == "__main__":
    hunt()
