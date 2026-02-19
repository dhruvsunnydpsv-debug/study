import os
import requests
import io
import json
import time
from supabase import create_client
import google.generativeai as genai
from pypdf import PdfReader

# --- SECRETS FETCHING ---
# This is the massive upgrade. It automatically pulls your hidden keys from GitHub Actions.
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_KEY]):
    print("❌ ERROR: Missing API Keys. Make sure they are in GitHub Secrets!")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_unprocessed_paper():
    # Grab 1 random paper to process per run to keep it fast and avoid timeouts
    res = supabase.table("source_papers").select("*").limit(1).execute()
    return res.data[0] if res.data else None

def extract_questions_with_ai(text, subject, chapter):
    prompt = f"""
    You are an expert CBSE Class 9 Exam Creator. Analyze this {subject} paper snippet for the chapter '{chapter}'.
    
    CBSE 2026 PATTERN RULES:
    - Section A: 1 Mark (MCQs/Objective)
    - Section B: 2 Marks (Very Short)
    - Section C: 3 Marks (Short)
    - Section D: 5 Marks (Long)
    - Section E: 4 Marks (Case-Based)

    Extract up to 10 distinct, high-quality questions.
    Return ONLY a raw JSON array. No markdown blocks, no backticks, no extra text.
    Format:
    [{{
      "question_text": "...",
      "difficulty": "Easy",
      "marks": 2,
      "section": "Section B",
      "type": "Theory"
    }}]
    
    TEXT:
    {text[:10000]}
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"⚠️ AI Parsing Error: {e}")
        return []

def run():
    print("🚀 --- VERIX AI PROCESSOR V2 STARTING ---")
    paper = get_unprocessed_paper()
    if not paper:
        print("No papers found in database.")
        return

    print(f"📄 Target Paper: {paper.get('file_name', 'Unknown')}")
    
    try:
        # 1. Download & Read PDF
        res = requests.get(paper['file_url'], timeout=15)
        reader = PdfReader(io.BytesIO(res.content))
        text = "".join([p.extract_text() for p in reader.pages[:3]])
        
        if len(text.strip()) < 50:
            print("⚠️ Skipping: Not enough text found (might be a scanned image).")
            return

        # 2. Ask Gemini to Extract Questions
        print("🧠 Asking Gemini to extract questions according to 2026 Pattern...")
        questions = extract_questions_with_ai(text, paper['subject'], paper['chapter'])
        
        if not questions:
            print("⚠️ No questions extracted. Moving on.")
            return

        # 3. Save to Supabase with Smart Anti-Repeat Logic
        saved_count = 0
        for q in questions:
            q.update({"subject": paper['subject'], "chapter": paper['chapter']})
            
            # Check if question already exists
            existing = supabase.table("question_bank").select("id, appearance_count").eq("question_text", q['question_text']).execute()
            
            if existing.data:
                new_count = (existing.data[0]['appearance_count'] or 1) + 1
                supabase.table("question_bank").update({"appearance_count": new_count}).eq("id", existing.data[0]['id']).execute()
                print("   📈 Increased importance for repeated question.")
            else:
                supabase.table("question_bank").insert(q).execute()
                print(f"   ✅ Saved: [{q['section']}] {q['question_text'][:30]}...")
                saved_count += 1
        
        print(f"🎉 Success! Added {saved_count} new questions to the bank.")

    except Exception as e:
        print(f"❌ Critical Error processing paper: {e}")

if __name__ == "__main__":
    run()
