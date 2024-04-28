import requests
from bs4 import BeautifulSoup
import os
import shutil
import json
import re
# Define the initial URL to scrape

initial_url = 'https://siomar.net/product-category/e-liquids/'
lsurls = []
lsurls.append(initial_url)
filetext = 'siomar.txt'
# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links - adjust the selector to find the required links
    links = soup.find_all(class_='next page-numbers', href=True)
    
    # Follow each link (you may want to add conditions here)
    
    for link in links:   
        # Construct the full URL if necessary
        next_page_url = link['href']
        print(next_page_url)
        if not next_page_url.startswith('http'):
            next_page_url = requests.compat.urljoin(url, next_page_url)
        try:
            x = link['href']
            print(x,"XX")
            if x is not None:
                lsurls.append(next_page_url)
                print(f'Following link to: {next_page_url}')
                print(lsurls)
                scrape_page(next_page_url)  # Recursive call to scrape the next page
                            
        except:
            pass
    
# Start scraping from the initial URL
scrape_page(initial_url)

with open(filetext,'w') as f:        
                f.writelines([f"{line}\n" for line in lsurls])
				


