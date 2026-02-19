import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from supabase import create_client
from openai import OpenAI
import time

# 1. Setup Clients using GitHub Secrets
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
ai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_description(filename):
    """Uses your new OpenAI key to generate a clean title for the PDF"""
    response = ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Clean this filename into a study title: {filename}"}]
    )
    return response.choices[0].message.content

def hunt_to_supabase(base_url):
    headers = {'User-Agent': 'Mozilla/5.0 Chrome/91.0.4472.124 Safari/537.36'}
    
    print(f"Starting hourly hunt on {base_url}...")
    
    try:
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        count = 0
        for link in links:
            if link['href'].lower().endswith('.pdf'):
                pdf_url = urljoin(base_url, link['href'])
                filename = link['href'].split('/')[-1]
                
                # Get AI-enhanced title
                clean_title = get_ai_description(filename)
                
                # 2. Insert into Supabase Table (Make sure your table is named 'pdfs')
                data, count_resp = supabase.table("pdfs").insert({
                    "title": clean_title,
                    "url": pdf_url,
                    "subject": "General Study" 
                }).execute()
                
                count += 1
                print(f"Added to Supabase: {clean_title}")
                if count >= 100: break # Safety cap per hour
                time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Change this to any educational directory you want to hunt
    TARGET = "https://sedl.org/afterschool/toolkits/science/pdf/"
    hunt_to_supabase(TARGET)
