import requests
import time
from supabase import create_client

# --- HARDCODED CREDENTIALS (TO FORCE IT TO WORK) ---
SUPABASE_URL = "https://wfegoasrtbhpursgcvh.supabase.co"
# Your Anon Key
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
# Your Serper Key
SERPER_KEY = "08f33a092d4657bd7ef7da25237b2d40703b9698"

print("--- INITIALIZING ---")
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase Client Created")
except Exception as e:
    print(f"❌ CRITICAL: Failed to create client: {e}")
    exit(1)

def hunt():
    print("--- STARTING SEARCH ---")
    # searching for just ONE thing first to prove it works
    query = "filetype:pdf class 9 maths rationalised syllabus 2025 question paper"
    
    headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}
    
    try:
        print(f"🔎 Sending query to Serper...")
        response = requests.post("https://google.serper.dev/search", json={"q": query, "num": 10}, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ API ERROR: {response.text}")
            return

        results = response.json().get('organic', [])
        print(f"✅ Found {len(results)} links!")

        if len(results) == 0:
            print("⚠️ Search worked but found 0 results. Try changing the query.")

        for item in results:
            print(f"   -> Saving: {item.get('title')}")
            data = {
                "file_name": item.get('title'),
                "file_url": item.get('link'),
                "subject": "Maths",
                "chapter": "General"
            }
            
            # ATTEMPTING SAVE
            try:
                # Using 'source_papers' matching your screenshot
                result = supabase.table("source_papers").upsert(data, on_conflict="file_url").execute()
                print("      ✅ SAVED to Database")
            except Exception as insert_error:
                print(f"      ❌ INSERT ERROR: {insert_error}")

    except Exception as e:
        print(f"❌ SCRIPT CRASHED: {e}")

if __name__ == "__main__":
    hunt()
