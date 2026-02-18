import requests
import time
from supabase import create_client

# --- CREDENTIALS (VERIFIED DOUBLE 'O') ---
# LOOK HERE: It is now "wfegoo" (double o)
SUPABASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
SERPER_KEY = "08f33a092d4657bd7ef7da25237b2d40703b9698"

# 1. TEST CONNECTION
print(f"--- CONNECTING TO: {SUPABASE_URL} ---")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Test Insert
    print("Testing connection...")
    # This row proves it works
    test_data = {"file_name": "TYPO_IS_FIXED", "file_url": "http://double-o-success.com", "subject": "Debug", "chapter": "Debug"}
    supabase.table("source_papers").upsert(test_data, on_conflict="file_url").execute()
    print("✅ SUCCESS! The double-o URL is working.")

except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    exit(1)

# 2. THE HUNT
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
            try:
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
                        pass
            except Exception as e:
                print(f"Search Error: {e}")
            
            time.sleep(1)

if __name__ == "__main__":
    hunt()
