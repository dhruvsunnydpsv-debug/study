import os
import requests
import io
import json
import time
from supabase import create_client
from openai import OpenAI
from pypdf import PdfReader

# --- SECRETS FROM ENVIRONMENT ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY]):
    print("❌ ERROR: Missing API Keys (SUPABASE_URL, SUPABASE_KEY, or OPENAI_API_KEY).")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
ai = OpenAI(api_key=OPENAI_API_KEY)

BATCH_SIZE = 50  # How many source papers to process per run

def get_unprocessed_papers():
    res = supabase.table("source_papers").select("*").eq("is_processed", False).limit(BATCH_SIZE).execute()
    return res.data

def mark_as_processed(paper_id):
    supabase.table("source_papers").update({"is_processed": True}).eq("id", paper_id).execute()

def extract_questions_with_ai(text, subject, chapter):
    prompt = f"""You are an expert CBSE Exam Creator for Class 9. Analyze the following {subject} paper snippet for the chapter '{chapter}'.

Extract up to 10 distinct, high-quality questions suitable for CBSE Class 9 board exams.

For each question, assign:
- "difficulty": one of "Easy", "Medium", or "Hard"

Return ONLY a valid JSON array. No markdown, no explanation. Format:
[
  {{"question_text": "...", "difficulty": "Easy"}},
  {{"question_text": "...", "difficulty": "Medium"}}
]

TEXT:
{text[:8000]}"""

    try:
        response = ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=3000
        )
        raw = response.choices[0].message.content.strip()
        # Clean markdown fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        print(f"⚠️ AI Parsing Error: {e}")
        return []

def run():
    print(f"🚀 --- QUESTION PROCESSOR STARTING (Batch Size: {BATCH_SIZE}) ---")
    papers = get_unprocessed_papers()

    if not papers:
        print("🎉 No unprocessed papers found! The queue is empty.")
        return

    print(f"📦 Found {len(papers)} papers in this batch.")
    total_questions = 0

    for index, paper in enumerate(papers):
        print(f"\n📄 [{index+1}/{len(papers)}] Processing: {paper.get('file_name', 'Unknown')}")

        try:
            # 1. Download & Read PDF
            res = requests.get(paper['file_url'], timeout=15)

            # Skip HTML/Drive links that aren't real PDFs
            content_start = res.content[:10].lower()
            if content_start.startswith(b'<!doc') or content_start.startswith(b'<html'):
                print("⚠️ Skipping: Link is a webpage, not a PDF.")
                mark_as_processed(paper['id'])
                continue

            reader = PdfReader(io.BytesIO(res.content))
            text = "".join([p.extract_text() or "" for p in reader.pages[:3]])

            if len(text.strip()) < 50:
                print("⚠️ Skipping: Not enough text extracted.")
                mark_as_processed(paper['id'])
                continue

            # 2. Extract Questions via OpenAI
            print("🧠 Asking GPT-4o-mini to extract questions...")
            questions = extract_questions_with_ai(text, paper['subject'], paper['chapter'])

            # 3. Save to Supabase question_bank
            if questions:
                saved = 0
                for q in questions:
                    row = {
                        "question_text": q.get("question_text", ""),
                        "difficulty": q.get("difficulty", "Medium"),
                        "subject": paper['subject'],
                        "chapter": paper['chapter']
                    }
                    try:
                        supabase.table("question_bank").insert(row).execute()
                        saved += 1
                    except Exception as e:
                        print(f"  ⚠️ Insert error: {e}")

                total_questions += saved
                print(f"   ✅ Added {saved} questions (Total: {total_questions})")

            # 4. Mark source paper as processed
            mark_as_processed(paper['id'])

            # 5. Pause to respect rate limits
            print("   ⏳ Pausing 2s...")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error processing paper: {e}")
            mark_as_processed(paper['id'])

    print(f"\n✅ Batch complete! Total questions added: {total_questions}")

if __name__ == "__main__":
    run()
