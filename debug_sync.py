
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
    "Content-Type": "application/json"
}

FILES = ["seed_maths.json", "seed_science.json"]

def sync_file(filename):
    print(f"Syncing {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        if not questions: return

        subject = questions[0].get('subject')
        if subject:
            print(f"Cleaning existing questions for {subject}...")
            del_url = f"{BASE_URL}?subject=eq.{urllib.parse.quote(subject)}"
            req = urllib.request.Request(del_url, method='DELETE', headers=HEADERS)
            try:
                with urllib.request.urlopen(req) as response:
                    print(f"  Delete status: {response.status}")
            except urllib.error.HTTPError as e:
                print(f"  Delete failed: {e.status} - {e.read().decode('utf-8')}")

        # Batch insert
        print(f"Inserting {len(questions)} questions...")
        data = json.dumps(questions).encode('utf-8')
        req = urllib.request.Request(BASE_URL, data=data, method='POST', headers=HEADERS)
        try:
            with urllib.request.urlopen(req) as response:
                print(f"  Insert status: {response.status}")
        except urllib.error.HTTPError as e:
            print(f"  Insert failed: {e.status} - {e.read().decode('utf-8')}")
            
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    for f in FILES:
        sync_file(f)
