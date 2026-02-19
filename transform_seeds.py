
import json
import os

FILES = [
    "seed_maths.json",
    "seed_science.json",
    "seed_sst.json",
    "seed_english.json",
    "seed_hindi.json",
    "seed_sanskrit.json",
    "seed_cs.json"
]

def transform_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_data = []
    for q in data:
        # Move image_url into question_text
        img_url = q.pop('image_url', '')
        if img_url:
            q['question_text'] = q['question_text'] + f" [Image: {img_url}]"
        
        # Ensure only supported keys exist in the dict for batch insert
        # Based on OpenAPI spec: id, paper_id, question_text, subject, chapter, difficulty, is_rationalised, appearance_count
        filtered_q = {
            'question_text': q.get('question_text', ''),
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
