import os
import requests
import logging
import time
import random
from typing import List, Dict, Any, Optional
from supabase import create_client, Client

# --- 1. CONFIGURATION ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("interceptor.log"), logging.StreamHandler()]
)

# --- 2. TARGET API ENDPOINTS (Placeholder / Simulated Heist) ---
# In a real scenario, these would be the internal API endpoints discovered via devtools
TARGET_APIS = [
    {"url": "https://api.ncertbooks.guru/v1/questions/science-case-studies", "subject": "Science", "marks": 4},
    {"url": "https://api.ncertbooks.guru/v1/questions/maths-competency", "subject": "Mathematics", "marks": 4},
    {"url": "https://api.ncertbooks.guru/v1/questions/sst-long-answers", "subject": "Social Science", "marks": 5},
]

# --- 3. DYNAMIC BALANCING (Smart Hunt) ---
def get_inventory_audit():
    try:
        response = supabase.table("class9_question_bank").select("subject, marks, sub_subject").execute()
        data = response.data or []
        audit = {}
        for row in data:
            sub = row['subject']
            m = row['marks'] or 1
            ss = row.get('sub_subject', 'General')
            if sub not in audit: audit[sub] = {}
            if m not in audit[sub]: audit[sub][m] = {'count': 0, 'sub_subjects': {}}
            audit[sub][m]['count'] += 1
            if ss not in audit[sub][m]['sub_subjects']: audit[sub][m]['sub_subjects'][ss] = 0
            audit[sub][m]['sub_subjects'][ss] += 1
        return audit
    except Exception as e:
        logging.error(f"Audit failed: {e}")
        return {}

def should_skip(subject: str, marks: int, audit: Dict):
    sub_data = audit.get(subject, {})
    total_count = sum(m_data['count'] for m_data in sub_data.values())
    if total_count < 50: return False
    mcq_count = sub_data.get(1, {}).get('count', 0)
    ratio = mcq_count / total_count
    if marks == 1 and ratio > 0.8:
        return True
    return False

def detect_sub_subject(text: str, subject: str) -> str:
    text = text.lower()
    if subject == 'Science':
        if any(k in text for k in ['force', 'motion', 'gravity', 'sound', 'energy']): return 'Physics'
        if any(k in text for k in ['atom', 'matter', 'chemical', 'element']): return 'Chemistry'
        if any(k in text for k in ['cell', 'tissue', 'organism', 'disease']): return 'Biology'
    if subject == 'Social Science':
        if any(k in text for k in ['french', 'russian', 'hitler']): return 'History'
        if any(k in text for k in ['drainage', 'climate', 'population']): return 'Geography'
        if any(k in text for k in ['constitution', 'democracy']): return 'Political Science'
        if any(k in text for k in ['poverty', 'food', 'market']): return 'Economics'
    return 'General'

# --- 4. EXECUTION ---
def run_api_interceptor():
    logging.info("VERIX API INTERCEPTOR — INITIATING JSON HEIST (V3.5)")
    audit = get_inventory_audit()
    
    for api in TARGET_APIS:
        if should_skip(api["subject"], api["marks"], audit):
            logging.info(f"  [Balancer] Skipping {api['subject']} {api['marks']}m hunting — quota meta.")
            continue
            
        try:
            logging.info(f"  [Interceptor] Targeting {api['url']}...")
            
            # Simulated fetch
            mock_data = [
                {
                    "subject": api["subject"],
                    "chapter": "API Intercepted Data",
                    "question_text": f"Analyze the following {api['subject']} case scenario involving {['Physics', 'Chemistry', 'Biology'][random.randint(0,2)] if api['subject'] == 'Science' else 'History'} concepts.",
                    "correct_answer": "Refer to Section Analysis",
                    "marks": api["marks"],
                    "question_type": "Case-Based" if api["marks"] == 4 else "Subjective",
                    "source_reference": "API Interceptor v3.5"
                }
            ]
            
            for item in mock_data:
                # V3.5 Enrichment
                item["sub_subject"] = detect_sub_subject(item["question_text"], item["subject"])
                item["word_limit"] = "80-120 words" if item["marks"] >= 5 else ("50-80 words" if item["marks"] >= 3 else None)
                item["diagram_required"] = (item["marks"] >= 5 and item["subject"] in ['Science', 'Mathematics'])
                
                supabase.table("class9_question_bank").insert(item).execute()
                logging.info(f"  [Secured] JSON Asset: {api['subject']} ({api['marks']}m) | Sub: {item['sub_subject']}")
                
        except Exception as e:
            logging.error(f"  [Error] Intercept failed for {api['url']}: {e}")

if __name__ == "__main__":
    run_api_interceptor()

if __name__ == "__main__":
    run_api_interceptor()
