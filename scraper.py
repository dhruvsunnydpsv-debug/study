import requests
from bs4 import BeautifulSoup
import time

def scrape_study_materials(base_url):
    materials_scraped = []
    page_number = 1
    
    # User-Agent helps ensure your own server doesn't block the request as a generic bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Keep looping until we hit at least 100 study items
    while len(materials_scraped) < 100:
        print(f"Scanning page {page_number}... (Total items so far: {len(materials_scraped)})")
        
        # Pagination logic: adjust this based on how your site's URL structure is built
        # Examples: ?page=1, /notes/page/1, ?subject=maths&page=1
        url = f"{base_url}?page={page_number}" 
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- UPDATE THIS SELECTOR ---
            # Replace '.exam-question' with the actual HTML class used on your website
            # For example, it might be '.biology-note', '.flashcard', or '.syllabus-item'
            page_items = soup.select('.exam-question') 
            
            # Break the loop if we run out of pages before hitting 100
            if not page_items:
                print("No more study materials found on this page. Exiting loop.")
                break
                
            for item in page_items:
                # Extracting the text content of the study item
                extracted_data = item.get_text(strip=True)
                
                if extracted_data:
                    materials_scraped.append(extracted_data)
                
                # Stop immediately once we secure 100 items
                if len(materials_scraped) >= 100:
                    break
            
            page_number += 1
            time.sleep(2) # 2-second pause to avoid overloading your own server
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page_number}: {e}")
            break

    return materials_scraped

if __name__ == "__main__":
    # Your new study website URL
    TARGET_URL = "https://study.dhruvshah.co" 
    
    print(f"Starting scraper for {TARGET_URL}...")
    results = scrape_study_materials(TARGET_URL)
    
    print(f"\nSuccessfully scraped {len(results)} items!")
    
    print("\nHere are the last few items scraped to verify the count:")
    for i, res in enumerate(results[-5:], start=len(results)-4):
        print(f"{i}: {res}")
