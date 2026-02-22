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

BATCH_SIZE = 50

# ============ VERIX CHAPTER → BRANCH MAPPING ============
SCIENCE_BRANCH_MAP = {
    "Motion": "Physics", "Force and Laws of Motion": "Physics",
    "Gravitation": "Physics", "Work and Energy": "Physics", "Sound": "Physics",
    "Matter in Our Surroundings": "Chemistry", "Is Matter Around Us Pure": "Chemistry",
    "Atoms and Molecules": "Chemistry", "Structure of the Atom": "Chemistry",
    "The Fundamental Unit of Life": "Biology", "Tissues": "Biology",
    "Improvement in Food Resources": "Biology", "Natural Resources": "Biology"
}

MATHS_WEIGHTAGE_MAP = {
    "Number Systems": "Number Systems", "Polynomials": "Algebra",
    "Coordinate Geometry": "Coordinate Geometry",
    "Linear Equations in Two Variables": "Algebra",
    "Introduction to Euclids Geometry": "Geometry", "Lines and Angles": "Geometry",
    "Triangles": "Geometry", "Quadrilaterals": "Geometry", "Circles": "Geometry",
    "Constructions": "Geometry", "Herons Formula": "Mensuration",
    "Heron's Formula": "Mensuration", "Surface Areas and Volumes": "Mensuration",
    "Statistics": "Statistics & Probability", "Probability": "Statistics & Probability"
}

SST_WEIGHTAGE_MAP = {
    "The French Revolution": "History",
    "Socialism in Europe and the Russian Revolution": "History",
    "Nazism and the Rise of Hitler": "History",
    "Forest Society and Colonialism": "History",
    "India Size and Location": "Geography", "Physical Features of India": "Geography",
    "Drainage": "Geography", "Climate": "Geography",
    "Natural Vegetation and Wildlife": "Geography", "Population": "Geography",
    "What is Democracy Why Democracy": "Political Science",
    "Constitutional Design": "Political Science",
    "Electoral Politics": "Political Science",
    "Working of Institutions": "Political Science",
    "Democratic Rights": "Political Science",
    "Democracy in the Contemporary World": "Political Science",
    "The Story of Village Palampur": "Economics",
    "People as Resource": "Economics",
    "Poverty as a Challenge": "Economics",
    "Food Security in India": "Economics"
}


def get_unprocessed_papers():
    res = supabase.table("source_papers").select("*").eq("is_processed", False).limit(BATCH_SIZE).execute()
    return res.data

def mark_as_processed(paper_id):
    supabase.table("source_papers").update({"is_processed": True}).eq("id", paper_id).execute()

def extract_questions_with_ai(text, subject, chapter):
    # Verix-enhanced prompt: extracts section, marks, diagram info
    prompt = f"""You are an expert CBSE Exam Creator for Class 9 (2025-26 pattern). Analyze the following {subject} paper snippet for the chapter '{chapter}'.

Extract up to 10 distinct, high-quality questions suitable for CBSE Class 9 board exams.

For each question, assign:
- "difficulty": one of "Easy", "Medium", or "Hard"
- "section": which CBSE paper section this fits:
  - "A" for MCQs (1 mark)
  - "B" for Very Short Answer (2 marks)
  - "C" for Short Answer (3 marks)
  - "D" for Long Answer (5 marks)
  - "E" for Case Study (4 marks)
- "marks": integer marks (1, 2, 3, 4, or 5)
- "diagram_required": boolean, true if question needs a diagram/figure

Return ONLY a valid JSON array. No markdown, no explanation. Format:
[
  {{"question_text": "...", "difficulty": "Easy", "section": "A", "marks": 1, "diagram_required": false}},
  {{"question_text": "...", "difficulty": "Hard", "section": "D", "marks": 5, "diagram_required": true}}
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
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        print(f"⚠️ AI Parsing Error: {e}")
        return []

def enrich_with_verix_fields(question, subject, chapter):
    """Add Verix audit engine metadata to a question."""
    q = dict(question)

    # Ensure section/marks defaults
    if "section" not in q:
        q["section"] = "A"
    if "marks" not in q:
        q["marks"] = 1
    if "diagram_required" not in q:
        q["diagram_required"] = False

    # Word limits based on section
    word_limits = {"B": "30-50 words", "C": "50-80 words", "D": "80-120 words"}
    if subject == "Social Science":
        word_limits = {"B": "40 words", "C": "60 words", "D": "120 words"}
    if q["section"] in word_limits:
        q["word_limit"] = word_limits[q["section"]]

    # Sub-branch / weightage area
    if subject == "Science":
        q["sub_branch"] = SCIENCE_BRANCH_MAP.get(chapter, "Physics")
    elif subject == "Maths":
        q["weightage_area"] = MATHS_WEIGHTAGE_MAP.get(chapter, "Algebra")
    elif subject == "Social Science":
        q["weightage_area"] = SST_WEIGHTAGE_MAP.get(chapter, "History")

    # Force diagram_required for Science Sec D
    if subject == "Science" and q["section"] == "D":
        q["diagram_required"] = True

    # Force diagram for Maths Geometry/Mensuration Sec D
    if subject == "Maths" and q["section"] == "D":
        area = MATHS_WEIGHTAGE_MAP.get(chapter, "")
        if area in ["Geometry", "Mensuration"]:
            q["diagram_required"] = True

    return q

def run():
    print(f"🚀 --- VERIX QUESTION PROCESSOR STARTING (Batch Size: {BATCH_SIZE}) ---")
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

            # 2. Extract Questions via OpenAI (Verix-enhanced)
            print("🧠 Asking GPT-4o-mini to extract questions (Verix mode)...")
            questions = extract_questions_with_ai(text, paper['subject'], paper['chapter'])

            # 3. Save to Supabase question_bank with Verix fields
            if questions:
                saved = 0
                for q in questions:
                    enriched = enrich_with_verix_fields(q, paper['subject'], paper['chapter'])
                    row = {
                        "question_text": enriched.get("question_text", ""),
                        "difficulty": enriched.get("difficulty", "Medium"),
                        "subject": paper['subject'],
                        "chapter": paper['chapter'],
                        "section": enriched.get("section", "A"),
                        "marks": enriched.get("marks", 1),
                        "diagram_required": enriched.get("diagram_required", False),
                        "is_rationalised": True
                    }
                    # Add optional fields
                    if "word_limit" in enriched:
                        row["word_limit"] = enriched["word_limit"]
                    if "sub_branch" in enriched:
                        row["sub_branch"] = enriched["sub_branch"]
                    if "weightage_area" in enriched:
                        row["weightage_area"] = enriched["weightage_area"]

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
