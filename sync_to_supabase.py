
import json
import urllib.request
import urllib.parse
import glob
import os

# Supabase Config
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
BASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co/rest/v1/question_bank"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def sync_all():
    files = glob.glob("seed_*.json")
    all_questions = []
    
    print(f"Loading {len(files)} seed files...")
    for filename in files:
        # Skip seed_data.json if we have more specific files, or just include it
        # Actually, let's include all but be careful about duplicates
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                all_questions.extend(data)
                print(f"  Loaded {len(data)} from {filename}")
            except Exception as e:
                print(f"  Error loading {filename}: {e}")

    if not all_questions:
        print("No questions found to sync.")
        return

    # Group by subject and grade (Composite Key)
    by_composite = {}
    for q in all_questions:
        sub = q.get('subject')
        grade = q.get('grade', 9)
        if not sub: continue
        comp = f"{sub}_{grade}"
        if comp not in by_composite: by_composite[comp] = []
        by_composite[comp].append(q)

    # Sync each composite subject
    for comp_sub, questions in by_composite.items():
        print(f"\nSyncing {len(questions)} questions for {comp_sub}...")
        
        # 1. DELETE existing questions for this composite subject
        print(f"  Cleaning existing questions for {comp_sub}...")
        params = urllib.parse.urlencode({'subject': f'eq.{comp_sub}'})
        del_url = f"{BASE_URL}?{params}"
        req_del = urllib.request.Request(del_url, method='DELETE', headers=HEADERS)
        try:
            with urllib.request.urlopen(req_del) as resp:
                if resp.status not in [200, 204]:
                    print(f"  Delete failed: {resp.status}")
        except Exception as e:
            print(f"  Delete error: {e}")

        # 2. POST (Batch Insert) new questions
        chunk_size = 100
        for i in range(0, len(questions), chunk_size):
            chunk = questions[i:i + chunk_size]
            # Prep chunk for insertion: set subject to composite, remove grade
            for item in chunk:
                # Store original for log if needed, but for DB we need composite
                orig_sub = item.get('subject')
                item['subject'] = comp_sub
                if 'grade' in item: del item['grade']
            
            data = json.dumps(chunk).encode('utf-8')
            req_post = urllib.request.Request(BASE_URL, data=data, method='POST', headers=HEADERS)
            try:
                with urllib.request.urlopen(req_post) as resp:
                    if resp.status in [201, 204, 200]:
                        print(f"  Synced chunk {i//chunk_size + 1}/{ (len(questions)-1)//chunk_size + 1}")
                    else:
                        print(f"  Post failed: {resp.status}")
            except Exception as e:
                print(f"  Post error: {e}")

if __name__ == "__main__":
    sync_all()
