import requests
import time
from supabase import create_client

# --- FIXED CREDENTIALS (Pre-filled for you) ---
# I added 'https://' and '.supabase.co' to your project ID so it works
SUPABASE_URL = "https://wfegoasrtbhpursgcvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
SERPER_KEY = "08f33a092d4657bd7ef7da25237b2d40703b9698"

# 1. TEST CONNECTION
print(f"--- CONNECTING TO: {SUPABASE_URL} ---")
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    # Simple test insert to prove it works
    test_data = {"file_name": "FINAL_TEST", "file_url": "http://success.com", "subject": "Debug", "chapter": "Debug"}
    supabase.table("source_papers").upsert(test_data, on_conflict="file_url").execute()
    print("✅ SUCCESS: Connected and saved a test row!")
except Exception as e:
    print(f"❌ CONNECTION ERROR: {e}")
    exit(1)

# 2. THE REAL HUNT
syllabus = {
    "Maths": ["Polynomials", "Number Systems", "Circles"],
    "Science": ["Motion", "Force and Laws of Motion", "Gravitation"]
}

def hunt():
    print("--- STARTING PAPER HUNT ---")
    for subject, chapters in syllabus.items():
        for chapter in chapters:
            query = f"filetype:pdf class 9 {subject} {chapter} question paper 2025"
            print(f"🔍 Searching: {chapter}...")
            
            headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}
            response = requests.post("https://google.serper.dev/search", json={"q": query, "num": 10}, headers=headers)
            results = response.json().get('organic', [])

            for item in results:
                data = {
                    "file_name": item.get('title'),
                    "file_url": item.get('link'),
                    "subject": subject,
                    "chapter": chapter
                }
                try:
                    supabase.table("source_papers").upsert(data, on_conflict="file_url").execute()
                    print(f"   -> Saved: {item.get('title')[:30]}...")
                except:
                    pass # Ignore duplicate errors
            
            time.sleep(1) # Be polite to API

if __name__ == "__main__":
    hunt()
