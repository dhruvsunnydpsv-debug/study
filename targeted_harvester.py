import os
import requests
from bs4 import BeautifulSoup
import logging
import time
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
import random

# --- 1. CONFIGURATION ---
URL = "https://wfegooasrtbhpursgcvh.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
supabase: Client = create_client(URL, KEY)

DIAGRAM_BUCKET = "question_diagrams"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("targeted_harvest.log"), logging.StreamHandler()]
)

# --- 2. TARGETED SOURCES (Case Studies & Diagrams) ---
TARGET_PAGES = [
    {"url": "https://www.ncertbooks.guru/case-study-questions-for-class-9-science/", "subject": "Science", "type": "Case"},
    {"url": "https://www.ncertbooks.guru/case-study-questions-for-class-9-maths/", "subject": "Mathematics", "type": "Case"},
    {"url": "https://www.ncertbooks.guru/mcq-questions-for-class-9-science-chapter-5-with-answers/", "subject": "Science", "chapter": "Fundamental Unit of Life", "type": "General"},
    {"url": "https://www.ncertbooks.guru/mcq-questions-for-class-9-science-chapter-6-with-answers/", "subject": "Science", "chapter": "Tissues", "type": "General"},
]

# --- 3. UTILITIES ---
def download_and_upload_diagram(image_url: str, subject: str) -> Optional[str]:
    try:
        headers = {
            'User-Agent': 'VerixTargetedHunter/2.1 (https://personalvault.dhruvshah.co; mailto:noc@dhruvshah.co)',
            'Accept': 'image/webp,*/*'
        }
        res = requests.get(image_url, headers=headers, stream=True, timeout=15)
        res.raise_for_status()
        
        ext = image_url.split('.')[-1].split('?')[0]
        if ext not in ['png', 'jpg', 'jpeg', 'webp', 'svg']: ext = 'png'
        filename = f"targeted_{int(time.time())}_{random.randint(1000,9999)}.{ext}"
        path = f"{subject.lower().replace(' ', '_')}/{filename}"
        
        supabase.storage.from_(DIAGRAM_BUCKET).upload(
            file=res.content,
            path=path,
            file_options={"content-type": f"image/{ext}"}
        )
        return str(supabase.storage.from_(DIAGRAM_BUCKET).get_public_url(path))
    except Exception as e:
        logging.error(f"Diagram error: {e}")
        return None

# --- 4. TARGETED SCRAPER LOGIC ---
class TargetedScraper:
    @staticmethod
    def hunt(url: str, subject: str) -> List[Dict[str, Any]]:
        results = []
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            paragraphs = soup.find_all(['p', 'div'], class_=False)
            
            for p in paragraphs:
                text = p.get_text().strip()
                is_case = "Case Study" in text or "(i)" in text and "(ii)" in text
                img = p.find_next('img') if is_case else p.find('img')
                diag_url = None
                if img and ('wikimedia' in img.get('src', '') or 'guru' in img.get('src', '')):
                    diag_url = img['src']
                
                if not is_case and not diag_url:
                    continue
                
                q_obj = {
                    "subject": subject,
                    "chapter": "Targeted Assets",
                    "question_text": text.split("Answer:")[0].strip(),
                    "correct_answer": "Solution in Diagram/Source",
                    "marks": 4 if is_case else 3,
                    "question_type": "Case-Based" if is_case else "Diagram-Based",
                    "diagram_url": diag_url,
                    "source": f"Targeted Hunter: {url}"
                }
                
                if len(q_obj["question_text"]) > 20:
                    results.append(q_obj)
        except Exception as e:
            logging.error(f"  [Hunter] Scrape failed: {e}")
        return results

# --- 5. EXECUTION ---
def run_targeted_pipeline():
    logging.info("VERIX TARGETED ASSET HUNTER — INITIATING (V3.3)")
    for target in TARGET_PAGES:
        assets = TargetedScraper.hunt(target["url"], target["subject"])
        for item in assets:
            try:
                if item["diagram_url"]:
                    public_url = download_and_upload_diagram(item["diagram_url"], item["subject"])
                    item["diagram_url"] = public_url
                
                payload = {
                    "subject": item["subject"], "chapter": item["chapter"],
                    "question_text": item["question_text"], "correct_answer": item["correct_answer"],
                    "marks": item["marks"], "question_type": item["question_type"],
                    "diagram_url": item["diagram_url"], "source": item["source"]
                }
                supabase.table("class9_question_bank").insert(payload).execute()
                logging.info(f"  [Ingested] {item['question_type']} asset for {item['subject']}")
                time.sleep(2)
            except Exception as e:
                if '23505' not in str(e): logging.error(f"  [Ingestion Fail] {e}")

if __name__ == "__main__":
    run_targeted_pipeline()
