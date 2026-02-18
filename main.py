import os
import requests
import time
from supabase import create_client

# GitHub Actions will feed these in from the 'env' section of your yml
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
SERPER_KEY = os.environ.get("SERPER_KEY")

supabase = create_client(URL, KEY)

# Your structured organization map
syllabus = {
    "Maths": ["Number Systems", "Polynomials", "Coordinate Geometry", "Lines and Angles", "Triangles", "Quadrilaterals", "Circles", "Herons Formula", "Surface Areas and Volumes", "Statistics"],
    "Science": ["Matter in Our Surroundings", "Is Matter Around Us Pure", "Atoms and Molecules", "Structure of the Atom", "Fundamental Unit of Life", "Tissues", "Motion", "Force and Laws of Motion", "Gravitation", "Work and Energy", "Sound", "Improvement in Food Resources"]
}

def hunt():
    for subject, chapters in syllabus.items():
        for chapter in chapters:
            # Searching for BOTH Theory and Questions to fill the library
            for search_type in ["theory notes", "question paper"]:
                print(f"🔍 Hunting: {subject} - {chapter} ({search_type})")
                
                query = f"filetype:pdf class 9 {subject} {chapter} rationalised syllabus 2025 2026 {search_type}"
                headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}
                
                try:
                    response = requests.post("https://google.serper.dev/search", json={"q": query, "num": 50}, headers=headers)
                    results = response.json().get('organic', [])

                    if not results:
                        print(f"⚠️ No results found for {chapter}")

                    for item in results:
                        data = {
                            "file_name": item.get('title'),
                            "file_url": item.get('link'),
                            "subject": subject,
                            "chapter": chapter
                        }
                        # Using 'source_papers' to match your Supabase table name
                        supabase.table("source_papers").upsert(data, on_conflict="file_url").execute()
                        
                except Exception as e:
                    print(f"❌ Error during search or insert: {e}")
                
                time.sleep(1) # Delay to stay under API limits

if __name__ == "__main__":
    hunt()
