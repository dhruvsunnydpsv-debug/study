
import json
import os
import requests

# OpenAI Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def clean_title_with_ai(raw_title):
    if not OPENAI_API_KEY:
        return raw_title # Fallback

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"Convert this raw educational filename into a clean, professional academic title: '{raw_title}'. Return ONLY the title."
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        resp = requests.post(OPENAI_URL, headers=headers, json=payload)
        return resp.json()['choices'][0]['message']['content'].strip().strip('"')
    except Exception as e:
        print(f"AI Cleaning Error: {e}")
        return raw_title

def process_file(filename):
    print(f"AI Processing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for q in data:
        # 1. Clean Question Title if it looks raw
        if "question_text" in q and len(q["question_text"]) < 50:
             # This is a placeholder for real filename-to-title logic
             pass
        
        # 2. Add Diagram Tag if missing but image_url exists
        if q.get("image_url") and "[Image:" not in q.get("question_text", ""):
            q["question_text"] = q["question_text"] + f" [Image: {q['image_url']}]"
            
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    # Example: Process all seed files
    import glob
    for f in glob.glob("seed_*.json"):
        process_file(f)
