import os
import requests
import json
from supabase import create_client

# --- SECRETS ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SERPER_KEY = os.environ.get("SERPER_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, SERPER_KEY]):
    print("❌ ERROR: Missing API Keys. Check GitHub Secrets.")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# The subjects and grades we want to hunt for
SEARCH_QUERIES = [
    {"grade": "10", "subject": "Science"},
    {"grade": "10", "subject": "Maths"},
    {"grade": "12", "subject": "Physics"},
    {"grade": "12", "subject": "Biology"}
]

def hunt_for_pdfs():
    print("🕵️‍♂️ --- VERIX AUTO-HUNTER STARTING ---")
    total_found = 0

    for item in SEARCH_QUERIES:
        grade = item["grade"]
        subject = item["subject"]
        
        # We use a special Google Search trick: "filetype:pdf"
        query = f"CBSE Class {grade} {subject} previous year question paper filetype:pdf"
        print(f"\n🔍 Searching Google for: {query}")

        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query, "num": 20}) # Ask for 20 results per search
        headers = {
            'X-API-KEY': SERPER_KEY,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            results = response.json().get('organic', [])

            for res in results:
                link = res.get('link', '')
                title = res.get('title', 'Unknown Paper')
                
                # Only grab actual direct PDF links
                if link.endswith('.pdf'):
                    # Check if we already have this link in our database
                    existing = supabase.table("source_papers").select("id").eq("file_url", link).execute()
                    
                    if not existing.data:
                        # Save the new finding to Supabase!
                        new_paper = {
                            "file_name": title[:50],
                            "file_url": link,
                            "subject": subject,
                            "chapter": "Mixed Previous Year", # Default chapter for full papers
                            "is_processed": False # Ready for processor.py to read!
                        }
                        supabase.table("source_papers").insert(new_paper).execute()
                        print(f"   ✅ Found & Saved: {link[:60]}...")
                        total_found += 1
                    else:
                        print("   ⏭️ Already have this one, skipping.")

        except Exception as e:
            print(f"❌ Search Error: {e}")

    print(f"\n🎉 Hunt Complete! Added {total_found} new PDFs to the database.")

if __name__ == "__main__":
    hunt_for_pdfs()
