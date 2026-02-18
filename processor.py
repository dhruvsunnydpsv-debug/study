import os
import requests
import io
import json
import time
from supabase import create_client
import google.generativeai as genai
from pypdf import PdfReader

# --- CONFIGURATION ---
SUPABASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
GEMINI_KEY = "AIzaSyAMzy-rpQ3xrqLV7MJSmRFSKOETVZM2Br4" # Your provided key

# Initialize Clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_unprocessed_paper():
    # Fetch a paper that exists but hasn't been processed into questions yet
    # (In a real scenario, we would check a 'processed' flag, but here we pick random for demo)
    response = supabase.table("source_papers").select("*").limit(1).execute()
    if response.data:
        return response.data[0]
    return None

def extract_text_from_pdf(url):
    try:
        response = requests.get(url)
        f = io.BytesIO(response.content)
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        return None

def analyze_with_ai(text, subject, chapter):
    prompt = f"""
    You are a strict teacher. I will give you text from a {subject} exam paper on {chapter}.
    Extract 5 distinct questions from it.
    
    Return ONLY valid JSON in this format:
    [
      {{
        "question_text": "The actual question goes here",
        "difficulty": "Easy", 
        "marks": 1,
        "type": "MCQ"
      }},
      {{
        "question_text": "Another question...",
        "difficulty": "Hard",
        "marks": 5,
        "type": "Theory"
      }}
    ]
    
    Rules:
    - Difficulty must be 'Easy', 'Medium', or 'Hard'.
    - Type must be 'MCQ', 'Theory', or 'Numerical'.
    - Do not include markdown formatting like ```json.
    
    Here is the text:
    {text[:10000]} 
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's pure JSON
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return []

def run_processor():
    print("--- 🧠 STARTING AI PROCESSOR ---")
    
    paper = get_unprocessed_paper()
    if not paper:
        print("No papers found to process.")
        return

    print(f"📄 Processing: {paper['file_name']} ({paper['chapter']})")
    
    # 1. Extract Text
    pdf_text = extract_text_from_pdf(paper['file_url'])
    if not pdf_text or len(pdf_text) < 50:
        print("⚠️ PDF was empty or unreadable (scanned image). Skipping.")
        return

    # 2. Send to AI
    print("🤖 Analyzing with Gemini...")
    questions = analyze_with_ai(pdf_text, paper['subject'], paper['chapter'])
    
    # 3. Save to Question Bank
    if questions:
        print(f"✅ Extracted {len(questions)} questions!")
        for q in questions:
            # Add metadata from the source paper
            q['source_paper_id'] = paper['id'] # Needs ID from source_papers
            q['subject'] = paper['subject']
            q['chapter'] = paper['chapter']
            
            try:
                supabase.table("question_bank").insert(q).execute()
                print(f"   -> Saved: {q['difficulty']} question ({q['marks']} marks)")
            except Exception as e:
                print(f"   ❌ Save Error: {e}")
    else:
        print("⚠️ AI found no questions.")

if __name__ == "__main__":
    run_processor()
