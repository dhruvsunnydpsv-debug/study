import os
import requests
import time
from supabase import create_client

# --- SECRETS FROM ENVIRONMENT (set via GitHub Secrets) ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SERPER_KEY = os.environ.get("SERPER_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, SERPER_KEY]):
    print("❌ CRITICAL ERROR: Missing API Keys. Set SUPABASE_URL, SUPABASE_KEY, and SERPER_KEY as environment variables.")
    exit(1)

# 1. SETUP CLIENT
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    exit(1)


# 2. THE COMPLETE CLASS 9 SYLLABUS
syllabus = {
    "Maths": [
        "Number Systems", "Polynomials", "Coordinate Geometry", 
        "Linear Equations in Two Variables", "Introduction to Euclids Geometry", 
        "Lines and Angles", "Triangles", "Quadrilaterals", "Circles", 
        "Herons Formula", "Surface Areas and Volumes", "Statistics"
    ],
    "Science": [
        "Matter in Our Surroundings", "Is Matter Around Us Pure", 
        "Atoms and Molecules", "Structure of the Atom", 
        "The Fundamental Unit of Life", "Tissues", "Motion", 
        "Force and Laws of Motion", "Gravitation", "Work and Energy", 
        "Sound", "Improvement in Food Resources"
    ],
    "Social Science": [
        "The French Revolution", "Socialism in Europe and the Russian Revolution",
        "Nazism and the Rise of Hitler", "Forest Society and Colonialism",
        "India Size and Location", "Physical Features of India", "Drainage",
        "Climate", "Natural Vegetation and Wildlife", "Population",
        "What is Democracy Why Democracy", "Constitutional Design", 
        "Electoral Politics", "Working of Institutions", "Democratic Rights",
        "The Story of Village Palampur", "People as Resource", 
        "Poverty as a Challenge", "Food Security in India"
    ],
    "English": [
        "Beehive Prose", "Beehive Poems", "Moments Supplementary Reader", 
        "English Reading Comprehension", "English Writing Skills", "English Grammar"
    ],
    "Hindi": [
        "Kshitij", "Sparsh", "Kritika", "Sanchayan", "Hindi Vyakaran"
    ]
}

# 3. SEARCH PARAMETERS
years = ["2025", "2024", "2023", "2022"]
doc_types = ["question paper", "sample paper", "worksheet"]

def hunt():
    print("--- STARTING ULTIMATE CLASS 9 HUNT ---")
    total_found = 0

    for subject, chapters in syllabus.items():
        print(f"📘 STARTING SUBJECT: {subject}")
        
        for chapter in chapters:
            for year in years:
                for doc_type in doc_types:
                    # Specific query for maximum yield
                    query = f"filetype:pdf class 9 {subject} {chapter} {doc_type} {year} download"
                    
                    print(f"🔍 Hunting: {chapter} | {doc_type} | {year}...")
                    
                    headers = {'X-API-KEY': SERPER_KEY, 'Content-Type': 'application/json'}
                    try:
                        # Requesting 100 results per search
                        response = requests.post("https://google.serper.dev/search", json={"q": query, "num": 100}, headers=headers)
                        results = response.json().get('organic', [])

                        if not results:
                            continue

                        count = 0
                        for item in results:
                            data = {
                                "file_name": item.get('title'),
                                "file_url": item.get('link'),
                                "subject": subject,
                                "chapter": chapter
                            }
                            try:
                                # "Dumb" insert to force data in (bypassing unique constraint errors)
                                supabase.table("source_papers").insert(data).execute()
                                count += 1
                            except:
                                pass # Skip duplicates silently
                        
                        total_found += count
                        if count > 0:
                            print(f"   ✅ +{count} papers. (Total: {total_found})")

                    except Exception as e:
                        print(f"   ❌ Network/API Error: {e}")
                    
                    # Sleep is CRITICAL here to avoid getting banned by Google or Serper
                    time.sleep(1.5)

if __name__ == "__main__":
    hunt()
