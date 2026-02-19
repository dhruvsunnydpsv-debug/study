
import json
import urllib.request
import urllib.parse
import sys

# Supabase Config
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
BASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co/rest/v1/question_bank"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

FILES = [
    "seed_maths.json",
    "seed_science.json",
    "seed_sst.json",
    "seed_english.json",
    "seed_hindi.json",
    "seed_sanskrit.json",
    "seed_cs.json"
]

def sync_file(filename):
    print(f"Syncing {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        if not questions:
            print("  Empty file.")
            return

        subject = questions[0].get('subject')
        if subject:
            print(f"Cleaning existing questions for {subject}...")
            # urllib DELETE request
            params = urllib.parse.urlencode({'subject': f'eq.{subject}'})
            del_url = f"{BASE_URL}?{params}"
            req = urllib.request.Request(del_url, method='DELETE', headers=HEADERS)
            with urllib.request.urlopen(req) as response:
                if response.status not in [200, 204]:
                    print(f"  Delete failed: {response.status}")

        # Batch insert - handle large payloads by chunking if needed, but 100-200 should be fine
        data = json.dumps(questions).encode('utf-8')
        req = urllib.request.Request(BASE_URL, data=data, method='POST', headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            if response.status in [201, 204, 200]:
                print(f"  Successfully synced {len(questions)} questions.")
            else:
                print(f"  Failed with status: {response.status}")
            
    except Exception as e:
        print(f"  Error processing {filename}: {e}")

if __name__ == "__main__":
    for f in FILES:
        sync_file(f)
