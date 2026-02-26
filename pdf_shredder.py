"""
VERIX PDF SHREDDER v1.0
========================
Enterprise-grade PDF ingestion pipeline for the Verix question bank.
Takes a PDF URL (or local file), rips it with PyMuPDF, sends chunks to
Gemini 1.5 Flash for strict JSON parsing, uploads diagrams to Supabase
Storage, and inserts rows into class9_question_bank.

Usage:
  python pdf_shredder.py <pdf_url_or_path> --subject "Science" --chapter "Motion"

Env vars required:
  SUPABASE_URL         - Your Supabase project URL
  SUPABASE_SERVICE_KEY - Service-role key (not anon key) for Storage write
  GEMINI_API_KEY       - Gemini API key
"""

import os
import sys
import re
import json
import logging
import argparse
import time
import io
import tempfile
import hashlib
import base64
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
import httpx
import google.generativeai as genai
from supabase import create_client, Client
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("shredder.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("PDFShredder")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
BUCKET_NAME = "question_diagrams"
PAGES_PER_CHUNK = 6  # Pages sent to Gemini at once
MAX_RETRIES = 3
RETRY_DELAY = 4  # seconds

# CBSE Class 9 subject names (canonical)
SUBJECT_ALIASES = {
    "science": "Science",
    "physics": "Science",
    "chemistry": "Science",
    "biology": "Science",
    "math": "Mathematics",
    "maths": "Mathematics",
    "mathematics": "Mathematics",
    "social": "Social Science",
    "sst": "Social Science",
    "history": "Social Science",
    "geography": "Social Science",
    "civics": "Social Science",
    "english": "English",
}

# ─────────────────────────────────────────────────────────────────────────────
# GEMINI SETUP
# ─────────────────────────────────────────────────────────────────────────────

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=genai.GenerationConfig(
        temperature=0.1,  # Low temp = reliable structured output
        max_output_tokens=8192,
    ),
)

SYSTEM_PROMPT = """You are a strict academic data extraction engine. 
Your ONLY job is to read the provided raw text ripped from an official CBSE/KVS 
educational PDF and extract questions into a precise JSON array.

CRITICAL RULES — DO NOT BREAK THESE:
1. DO NOT invent, generate, or hallucinate any questions. 
2. ONLY extract questions that genuinely appear in the source text.
3. DO NOT paraphrase or alter the academic substance of any question.
4. DO NOT include answer keys in question_text. Correct answers go in correct_answer.
5. If a question has options labelled (A)(B)(C)(D) or (a)(b)(c)(d), it is an MCQ.

OUTPUT FORMAT:
Return ONLY a valid JSON array. Nothing else. No markdown. No prose. No ```json fences.
Each object in the array must follow this exact schema:

{
  "subject": "Science" | "Mathematics" | "Social Science" | "English",
  "chapter": "<chapter name if identifiable, else 'Unknown'>",
  "question_text": "<exact question text>",
  "options": {"A": "...", "B": "...", "C": "...", "D": "..."} | null,
  "correct_answer": "<correct option letter or short answer or null>",
  "marks": <integer: 1, 2, 3, 4, or 5>,
  "question_type": "<MCQ | Short Answer | Long Answer | Case Study | Assertion-Reasoning | Map | Fill in the Blank>",
  "sub_subject": "<Physics | Chemistry | Biology | Algebra | Geometry | History | Geography | Civics | Economics | null>",
  "source_reference": "KVS Study Material" | "CBSE CBE Portal" | "NCERT Exemplar",
  "diagram_required": <true | false>,
  "difficulty": "Easy" | "Medium" | "Hard"
}

MARKS INFERENCE RULES (use if not explicitly stated):
- MCQ / Fill in the Blank → 1 mark
- Very Short Answer (1-2 lines) → 2 marks  
- Short Answer (3-4 lines) → 3 marks
- Case Study / Source-based → 4 marks
- Long Answer (detailed) → 5 marks

SUBJECT INFERENCE: Use the document context to infer subject. Physics/Chemistry/Biology maps to "Science".
"""

# ─────────────────────────────────────────────────────────────────────────────
# SUPABASE CLIENT
# ─────────────────────────────────────────────────────────────────────────────

sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def ensure_bucket():
    """Ensure the question_diagrams bucket exists."""
    try:
        buckets = sb.storage.list_buckets()
        names = [b.name for b in buckets]
        if BUCKET_NAME not in names:
            sb.storage.create_bucket(BUCKET_NAME, options={"public": True})
            log.info("Created storage bucket: %s", BUCKET_NAME)
    except Exception as e:
        log.warning("Could not verify bucket (may already exist): %s", e)


# ─────────────────────────────────────────────────────────────────────────────
# PDF DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────

def download_pdf(url_or_path: str) -> Path:
    """Download a PDF from URL or return local path."""
    if Path(url_or_path).exists():
        log.info("Using local PDF: %s", url_or_path)
        return Path(url_or_path)

    log.info("Downloading PDF from: %s", url_or_path)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    with httpx.Client(timeout=120, follow_redirects=True) as client:
        with client.stream("GET", url_or_path) as r:
            r.raise_for_status()
            for chunk in r.iter_bytes(chunk_size=65536):
                tmp.write(chunk)
    tmp.close()
    log.info("Downloaded to: %s", tmp.name)
    return Path(tmp.name)


# ─────────────────────────────────────────────────────────────────────────────
# IMAGE EXTRACTION & UPLOAD
# ─────────────────────────────────────────────────────────────────────────────

def upload_image(img_bytes: bytes, img_name: str) -> Optional[str]:
    """Upload an image to Supabase Storage and return its public URL."""
    try:
        path = f"diagrams/{img_name}"
        sb.storage.from_(BUCKET_NAME).upload(
            path,
            img_bytes,
            file_options={"content-type": "image/png", "upsert": "true"},
        )
        public_url = sb.storage.from_(BUCKET_NAME).get_public_url(path)
        log.info("Uploaded diagram: %s", public_url)
        return public_url
    except Exception as e:
        log.warning("Failed to upload image %s: %s", img_name, e)
        return None


def extract_page_images(page: fitz.Page, pdf_hash: str, page_num: int) -> list[dict]:
    """Extract all embedded images from a PDF page, return list of {bytes, name}."""
    images = []
    img_list = page.get_images(full=True)
    for img_index, img_info in enumerate(img_list):
        xref = img_info[0]
        try:
            base = page.parent.extract_image(xref)
            img_bytes = base["image"]
            ext = base.get("ext", "png")
            # Create a deterministic name based on PDF hash + page + index
            img_hash = hashlib.md5(img_bytes).hexdigest()[:8]
            name = f"{pdf_hash}_{page_num}_{img_index}_{img_hash}.png"
            # Convert to PNG if not already
            if ext != "png":
                try:
                    pil_img = Image.open(io.BytesIO(img_bytes))
                    buf = io.BytesIO()
                    pil_img.save(buf, format="PNG")
                    img_bytes = buf.getvalue()
                except Exception:
                    pass
            # Skip tiny decorative images (< 5KB)
            if len(img_bytes) < 5120:
                continue
            images.append({"bytes": img_bytes, "name": name})
        except Exception as e:
            log.debug("Could not extract image xref %d on page %d: %s", xref, page_num, e)
    return images


# ─────────────────────────────────────────────────────────────────────────────
# LLM PARSING
# ─────────────────────────────────────────────────────────────────────────────

def parse_chunk_with_gemini(
    raw_text: str,
    default_subject: str,
    default_chapter: str,
    page_images: list[dict],
) -> list[dict]:
    """Send a text chunk to Gemini and return parsed question list."""

    pages_context = (
        f"\n\nDocument context:\n- Default Subject: {default_subject}\n- Chapter: {default_chapter}"
    )
    prompt = SYSTEM_PROMPT + pages_context + "\n\n--- BEGIN RAW EXTRACTED TEXT ---\n" + raw_text + "\n--- END RAW EXTRACTED TEXT ---"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = model.generate_content(prompt)
            raw_json = response.text.strip()
            # Strip markdown code fences if Gemini adds them despite instructions
            raw_json = re.sub(r"^```(?:json)?\s*", "", raw_json)
            raw_json = re.sub(r"\s*```$", "", raw_json)
            questions = json.loads(raw_json)
            if not isinstance(questions, list):
                questions = [questions]
            log.info("Gemini returned %d questions for this chunk.", len(questions))
            return questions
        except json.JSONDecodeError as e:
            log.warning("Attempt %d: JSON parse error: %s", attempt, e)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            log.warning("Attempt %d: Gemini error: %s", attempt, e)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * attempt)

    log.error("All %d attempts failed for this chunk. Skipping.", MAX_RETRIES)
    return []


# ─────────────────────────────────────────────────────────────────────────────
# DATABASE INSERT
# ─────────────────────────────────────────────────────────────────────────────

VALID_SUBJECTS = {"Science", "Mathematics", "Social Science", "English"}
VALID_TYPES = {
    "MCQ", "Short Answer", "Long Answer", "Case Study",
    "Assertion-Reasoning", "Map", "Fill in the Blank",
}


def normalize_row(q: dict, default_subject: str, default_chapter: str, diagram_url: Optional[str] = None) -> Optional[dict]:
    """Validate and normalize a parsed question dict into DB row format."""
    question_text = (q.get("question_text") or "").strip()
    if not question_text or len(question_text) < 10:
        return None

    subject = q.get("subject", default_subject)
    if subject not in VALID_SUBJECTS:
        # Try alias lookup
        subject = SUBJECT_ALIASES.get(subject.lower(), default_subject)

    chapter = (q.get("chapter") or default_chapter or "Unknown").strip()
    marks = q.get("marks")
    if not isinstance(marks, int) or marks not in (1, 2, 3, 4, 5):
        marks = 1  # Safe default

    question_type = q.get("question_type", "Short Answer")
    if question_type not in VALID_TYPES:
        question_type = "Short Answer"

    options = q.get("options")
    if options and not isinstance(options, dict):
        options = None

    row = {
        "subject": subject,
        "chapter": chapter,
        "question_text": question_text,
        "options": options,
        "correct_answer": q.get("correct_answer"),
        "marks": marks,
        "question_type": question_type,
        "sub_subject": q.get("sub_subject"),
        "source_reference": q.get("source_reference", "KVS Study Material"),
        "difficulty": q.get("difficulty", "Medium"),
        "diagram_required": bool(q.get("diagram_required", False)),
        "diagram_url": diagram_url,
    }
    return row


def insert_questions(rows: list[dict]) -> int:
    """Insert rows into class9_question_bank using upsert (avoids duplicates)."""
    if not rows:
        return 0
    inserted = 0
    # Batch in groups of 50
    for i in range(0, len(rows), 50):
        batch = rows[i : i + 50]
        try:
            res = (
                sb.table("class9_question_bank")
                .upsert(batch, on_conflict="subject,chapter,question_text", ignore_duplicates=True)
                .execute()
            )
            inserted += len(batch)
        except Exception as e:
            log.error("Insert batch failed: %s", e)
    return inserted


# ─────────────────────────────────────────────────────────────────────────────
# SELF-BALANCING LOGIC
# ─────────────────────────────────────────────────────────────────────────────

MINIMUM_TARGETS = {
    ("Science", 1): 200,
    ("Science", 2): 60,
    ("Science", 3): 70,
    ("Science", 4): 30,
    ("Science", 5): 30,
    ("Mathematics", 1): 200,
    ("Mathematics", 2): 60,
    ("Mathematics", 3): 60,
    ("Mathematics", 4): 30,
    ("Mathematics", 5): 40,
    ("Social Science", 1): 200,
    ("Social Science", 3): 40,
    ("Social Science", 4): 30,
    ("Social Science", 5): 30,
    ("English", None): 100,
}


def check_balance(subject: str) -> dict:
    """Return current DB counts for the given subject, grouped by marks."""
    counts = {}
    for marks in [1, 2, 3, 4, 5]:
        try:
            res = (
                sb.table("class9_question_bank")
                .select("id", count="exact")
                .ilike("subject", f"%{subject}%")
                .eq("marks", marks)
                .execute()
            )
            counts[marks] = res.count or 0
        except Exception:
            counts[marks] = 0
    return counts


def get_deficit_summary(subject: str) -> list[tuple]:
    """Return list of (marks, deficit) for the given subject that are below target."""
    counts = check_balance(subject)
    deficits = []
    for marks, count in counts.items():
        target = MINIMUM_TARGETS.get((subject, marks), 0)
        if count < target:
            deficits.append((marks, target - count))
    return sorted(deficits, key=lambda x: x[1], reverse=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN SHREDDER ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def shred(pdf_url_or_path: str, subject: str, chapter: str = "Unknown"):
    ensure_bucket()

    pdf_path = download_pdf(pdf_url_or_path)
    pdf_hash = hashlib.md5(pdf_path.read_bytes()).hexdigest()[:10]

    log.info("=== Starting PDF Shredder ===")
    log.info("PDF: %s | Subject: %s | Hash: %s", pdf_url_or_path, subject, pdf_hash)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    log.info("Total pages: %d", total_pages)

    # Pre-flight balance check
    deficits = get_deficit_summary(subject)
    if deficits:
        log.info("Pre-flight balance check — deficit detected for %s:", subject)
        for marks, deficit in deficits:
            log.info("  %d-mark questions: need %d more", marks, deficit)
    else:
        log.info("Pre-flight: %s question bank is balanced. Running for top-up.", subject)

    all_rows = []
    total_inserted = 0
    page_images_global = []  # All images extracted from the whole PDF

    # Process pages in chunks
    for chunk_start in range(0, total_pages, PAGES_PER_CHUNK):
        chunk_end = min(chunk_start + PAGES_PER_CHUNK, total_pages)
        log.info("Processing pages %d–%d / %d ...", chunk_start + 1, chunk_end, total_pages)

        chunk_text = ""
        chunk_images = []

        for page_num in range(chunk_start, chunk_end):
            page = doc[page_num]
            chunk_text += f"\n\n[PAGE {page_num + 1}]\n"
            chunk_text += page.get_text("text")
            imgs = extract_page_images(page, pdf_hash, page_num + 1)
            chunk_images.extend(imgs)

        if not chunk_text.strip():
            log.debug("Empty chunk, skipping.")
            continue

        # Parse with Gemini
        parsed = parse_chunk_with_gemini(chunk_text, subject, chapter, chunk_images)

        # Upload images and build a mapping (image_index → url)
        uploaded_urls = []
        for img_info in chunk_images:
            url = upload_image(img_info["bytes"], img_info["name"])
            uploaded_urls.append(url)

        # Normalize and assign diagram URLs
        rows = []
        for i, q in enumerate(parsed):
            # Heuristic: assign first image in chunk to first diagram-requiring question
            diagram_url = None
            if q.get("diagram_required") and uploaded_urls:
                diagram_url = uploaded_urls[0]
            row = normalize_row(q, subject, chapter, diagram_url)
            if row:
                rows.append(row)

        if rows:
            n = insert_questions(rows)
            total_inserted += n
            log.info("Chunk %d–%d: inserted %d questions. Running total: %d", chunk_start + 1, chunk_end, n, total_inserted)
        else:
            log.info("Chunk %d–%d: no valid questions extracted.", chunk_start + 1, chunk_end)

        # Rate limit — avoid hammering Gemini API
        time.sleep(1.5)

    doc.close()

    # Post-run balance report
    log.info("=== PDF Shredder Complete ===")
    log.info("Total rows inserted: %d", total_inserted)
    counts = check_balance(subject)
    log.info("Post-run balance for %s:", subject)
    for marks, count in counts.items():
        target = MINIMUM_TARGETS.get((subject, marks), 0)
        status = "✅" if count >= target else "🚨"
        log.info("  %d-mark: %d / %d %s", marks, count, target, status)

    return total_inserted


# ─────────────────────────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Verix PDF Shredder — ingests Gov/KVS PDFs into class9_question_bank"
    )
    parser.add_argument("pdf", help="PDF URL or local file path")
    parser.add_argument(
        "--subject",
        default="Science",
        help="Subject: Science | Mathematics | Social Science | English (default: Science)",
    )
    parser.add_argument(
        "--chapter",
        default="Unknown",
        help="Chapter name override (default: Unknown — inferred from PDF)",
    )
    args = parser.parse_args()

    # Canonicalize subject
    subject_clean = SUBJECT_ALIASES.get(args.subject.lower(), args.subject)
    if subject_clean not in VALID_SUBJECTS:
        log.error("Invalid subject '%s'. Use one of: Science, Mathematics, Social Science, English", args.subject)
        sys.exit(1)

    total = shred(args.pdf, subject_clean, args.chapter)
    print(f"\n✅ Shredder complete. Inserted {total} questions for {subject_clean}.")


if __name__ == "__main__":
    main()
