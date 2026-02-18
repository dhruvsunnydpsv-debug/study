import requests
import time
from supabase import create_client

# --- CREDENTIALS (VERIFIED WORKING) ---
SUPABASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
SERPER_KEY = "08f33a092d4657bd7ef7da25237b2d40703b9698"

# 1. SETUP CLIENT
print(f"--- CONNECTING TO: {SUPABASE_URL} ---")
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
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
    
    # TEST INSERT (Using pure insert to bypass constraint error)
    print("Attempting test insert...")
    try:
        test_data = {"file_name": "FINAL_SUCCESS_TEST", "file_url": "http://final-test.com", "subject": "Debug", "chapter": "Debug"}
        supabase.table("source_papers").insert(test_data).execute()
        print("✅ SUCCESS! Test row saved to database.")
    except Exception as e:
        # If it fails, we print why but continue just in case
        print(f"⚠️ Test insert notice: {e}")

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
                        # CHANGED FROM UPSERT TO INSERT TO FIX YOUR ERROR
                        supabase.table("source_papers").insert(data).execute()
                        print(f"   -> Saved: {item.get('title')[:30]}...")
                    except Exception as e:
                        print(f"   ⚠️ Save Error: {e}")
            except Exception as e:
                print(f"Search Error: {e}")
            
            time.sleep(1)

if __name__ == "__main__":
    hunt()
