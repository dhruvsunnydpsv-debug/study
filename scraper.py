import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def hunt_1000_pdfs(base_url):
    folder_name = "downloaded_pdfs"
    os.makedirs(folder_name, exist_ok=True)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}
    pdf_count = 0
    target_count = 1000 # It will stop at 1000, or when it runs out of PDFs on the page
    
    print(f"Starting the hunt for PDFs on {base_url}...")
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status() # This is what triggered your 404 error earlier!
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            
            # Check if the link ends in .pdf
            if href.lower().endswith('.pdf'):
                pdf_url = urljoin(base_url, href)
                
                try:
                    # Create the file name
                    file_name = os.path.join(folder_name, href.split('/')[-1])
                    
                    print(f"Downloading: {pdf_url}")
                    pdf_response = requests.get(pdf_url, headers=headers, stream=True)
                    
                    # Save the file
                    with open(file_name, 'wb') as f:
                        for chunk in pdf_response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                
                    pdf_count += 1
                    print(f"Success! Got {pdf_count} PDFs so far.")
                    
                    if pdf_count >= target_count:
                        print("\nTarget reached! Shutting down hunter.")
                        return 
                        
                    time.sleep(1) # Pause to avoid getting IP banned
                        
                except Exception as e:
                    print(f"Could not download {pdf_url}: {e}")
                    
    except requests.exceptions.HTTPError as err:
        print(f"CRASH: The website URL is broken, dead, or blocking you. Error: {err}")
    except Exception as e:
        print(f"Failed to load the main website: {e}")

if __name__ == "__main__":
    # --- I CHANGED THIS TO A REAL, WORKING URL FOR TESTING ---
    # Once you see this work, change this URL to whatever actual site you want to steal PDFs from
    TARGET_WEBSITE = "https://sedl.org/afterschool/toolkits/science/pdf/" 
    
    hunt_1000_pdfs(TARGET_WEBSITE)
