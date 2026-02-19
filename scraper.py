import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from supabase import create_client
from openai import OpenAI
import time

# Client Setup using the Secrets you added to GitHub
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
ai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_clean_title(filename):
    """Uses OpenAI to make filenames look professional for your website"""
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Simplify this filename into a clean study title: {filename}"}]
        )
        return response.choices[0].message.content
    except:
        return filename

def start_hunt(target_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Starting hunt on {target_url}...")
    
    response = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    count = 0
    for link in soup.find_all('a', href=True):
        if link['href'].lower().endswith('.pdf'):
            full_url = urljoin(target_url, link['href'])
            filename = link['href'].split('/')[-1]
            
            clean_name = get_clean_title(filename)
            
            # Send data to Supabase table named 'pdfs'
            try:
                supabase.table("pdfs").insert({
                    "title": clean_name,
                    "url": full_url
                }).execute()
                print(f"Successfully stored: {clean_name}")
            except Exception as e:
                print(f"Skipping (might be a duplicate): {clean_name}")
            
            count += 1
            if count >= 100: break # Grab 100 per hour
            time.sleep(1) 

if __name__ == "__main__":
    # You can change this URL to any site you want to scrape
    start_hunt("https://sedl.org/afterschool/toolkits/science/pdf/")
