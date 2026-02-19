
import json
import os

# Automatically discover all seed_*.json files
import glob
FILES = glob.glob("seed_*.json")

def transform_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_data = []
    for q in data:
        # Move image_url into question_text if not already there
        img_url = q.get('image_url', '')
        q_text = q.get('question_text', '')
        
        if img_url and f"[Image: {img_url}]" not in q_text:
            q_text = q_text + f" [Image: {img_url}]"
        
        filtered_q = {
            'question_text': q_text,
            'subject': q.get('subject', ''),
            'chapter': q.get('chapter', ''),
            'difficulty': q.get('difficulty', ''),
            'is_rationalised': q.get('is_rationalised', True)
        }
        new_data.append(filtered_q)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    print(f"Transformed {filename}")

if __name__ == "__main__":
    for f in FILES:
        transform_file(f)
