import os
import requests
import io
import json
import time
from supabase import create_client
import google.generativeai as genai
from pypdf import PdfReader

# --- CREDENTIALS ---
SUPABASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
GEMINI_KEY = "AIzaSyAMzy-rpQ3xrqLV7MJSmRFSKOETVZM2Br4"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_unprocessed_paper():
    # Pick a random paper from your 6,532 sources
    res = supabase.table("source_papers").select("*").limit(1).execute()
    return res.data[0] if res.data else None

def analyze_paper_expertly(text, subject, chapter):
    # This prompt teaches Gemini the 2026 Board Marking Scheme
    prompt = f"""
    You are a CBSE Exam Expert. Analyze this {subject} paper on {chapter}.
    
    LATEST 2026 PATTERN RULES:
    - Section A: MCQs (1 Mark)
    - Section B: Very Short (2 Marks)
    - Section C: Short (3 Marks)
    - Section D: Long (5 Marks)
    - Section E: Case-Based (4 Marks)

    TASK:
    Extract 10 questions. For each, identify the correct Section and Difficulty.
    Difficulty Scale: 
    - Easy: Basic definitions/formulas.
    - Medium: Direct application/problems.
    - Hard: Complex proofs/HOTS questions.

    RETURN JSON ONLY:
    [{{
      "question_text": "...",
      "difficulty": "Hard",
      "marks": 5,
      "section": "Section D",
      "type": "Theory"
    }}]
    
    TEXT: {text[:10000]}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except: return []

def run_processor():
    print("--- 🧠 VERIX SMART PROCESSOR STARTING ---")
    paper = get_unprocessed_paper()
    if not paper: return

    try:
        # 1. Download & OCR
        res = requests.get(paper['file_url'], timeout=10)
        reader = PdfReader(io.BytesIO(res.content))
        text = "".join([p.extract_text() for p in reader.pages[:3]])
        
        # 2. AI Extraction
        print(f"🤖 Analyzing: {paper['file_name']}")
        questions = analyze_paper_expertly(text, paper['subject'], paper['chapter'])
        
        # 3. Smart Save
        for q in questions:
            q.update({"subject": paper['subject'], "chapter": paper['chapter']})
            
            # CHECK FOR DUPLICATES: If question exists, just increase its 'frequency'
            existing = supabase.table("question_bank").select("id, appearance_count").eq("question_text", q['question_text']).execute()
            
            if existing.data:
                new_count = (existing.data[0]['appearance_count'] or 1) + 1
                supabase.table("question_bank").update({"appearance_count": new_count}).eq("id", existing.data[0]['id']).execute()
                print("   📈 Increased frequency for repeated question.")
            else:
                supabase.table("question_bank").insert(q).execute()
                print(f"   ✅ Saved New {q['difficulty']} question.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_processor()
