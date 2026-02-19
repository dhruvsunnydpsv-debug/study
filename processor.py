import os
import requests
import io
import json
import time
from supabase import create_client
import google.generativeai as genai
from pypdf import PdfReader

# --- SECRETS FETCHING ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_KEY]):
    print("❌ ERROR: Missing API Keys.")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

BATCH_SIZE = 50 # How many papers to process in one GitHub run

def get_unprocessed_papers():
    # Only grab papers where is_processed is False
    res = supabase.table("source_papers").select("*").eq("is_processed", False).limit(BATCH_SIZE).execute()
    return res.data

def mark_as_processed(paper_id):
    # Check off the paper so we never process it again
    supabase.table("source_papers").update({"is_processed": True}).eq("id", paper_id).execute()

def extract_questions_with_ai(text, subject, chapter):
    prompt = f"""
    You are an expert CBSE Exam Creator. Analyze this {subject} paper snippet for the chapter '{chapter}'.
    Extract up to 10 distinct, high-quality questions based on the 2026 pattern.
    Return ONLY a raw JSON array. Format:
    [{{ "question_text": "...", "difficulty": "Easy", "marks": 2, "section": "Section B", "type": "Theory" }}]
    TEXT: {text[:10000]}
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"⚠️ AI Parsing Error: {e}")
        return []

def run():
    print(f"🚀 --- VERIX BATCH PROCESSOR STARTING (Batch Size: {BATCH_SIZE}) ---")
    papers = get_unprocessed_papers()
    
    if not papers:
        print("🎉 No unprocessed papers found! The database is full.")
        return

    print(f"📦 Found {len(papers)} papers in this batch.")

    for index, paper in enumerate(papers):
        print(f"\n📄 [{index+1}/{len(papers)}] Processing: {paper.get('file_name', 'Unknown')}")
        
        try:
            # 1. Download & Read PDF
            res = requests.get(paper['file_url'], timeout=15)
            
            # Catch HTML/Drive links that aren't real PDFs
            if res.content.startswith(b'<!doc') or res.content.startswith(b'<html'):
                print("⚠️ Skipping: Link is a webpage, not a direct PDF file.")
                mark_as_processed(paper['id']) # Mark as processed so it doesn't get stuck in a loop
                continue

            reader = PdfReader(io.BytesIO(res.content))
            text = "".join([p.extract_text() for p in reader.pages[:3]])
            
            if len(text.strip()) < 50:
                print("⚠️ Skipping: Not enough text found.")
                mark_as_processed(paper['id'])
                continue

            # 2. Extract Questions
            print("🧠 Asking Gemini to extract questions...")
            questions = extract_questions_with_ai(text, paper['subject'], paper['chapter'])
            
            # 3. Save to Supabase
            if questions:
                saved_count = 0
                for q in questions:
                    q.update({"subject": paper['subject'], "chapter": paper['chapter']})
                    # Simple insert for speed
                    supabase.table("question_bank").insert(q).execute()
                    saved_count += 1
                
                print(f"   ✅ Added {saved_count} questions to the bank.")
            
            # 4. Mark as Done!
            mark_as_processed(paper['id'])
            
            # 5. Sleep to prevent Gemini from blocking us for spamming
            print("   ⏳ Pausing for 4 seconds to respect AI limits...")
            time.sleep(4)

        except Exception as e:
            print(f"❌ Error processing paper: {e}")
            mark_as_processed(paper['id']) # Still mark it so a broken file doesn't break the whole loop

    print("\n✅ Batch complete!")

if __name__ == "__main__":
    run()
