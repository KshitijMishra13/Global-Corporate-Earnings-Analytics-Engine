import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. Setup browser headers to prevent getting blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# 2. Base URL for navigating the pages (100 companies per page)
base_url = "https://companiesmarketcap.com/most-profitable-companies/page/{}/"

# List to hold all rows of company data
all_companies = []

# Loop through the pages (approx. 110 pages for 10,859 companies)
max_pages = 110 

print("Starting target-specific scraper based on HTML structure...")

for page in range(1, max_pages + 1):
    url = base_url.format(page)
    print(f"Scraping Page {page} of {max_pages}...")
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Safely stopping. Server returned status: {response.status_code}")
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Locate the main table matching your HTML class configuration
        table = soup.find('table', class_='marketcap-table')
        if not table:
            print("Table structure not found on this page. Ending process.")
            break
            
        tbody = table.find('tbody')
        if not tbody:
            continue
            
        rows = tbody.find_all('tr')
        
        for row in rows:
            # RULE 1: Skip advertisement rows highlighted in your HTML layout
            if 'ad-tr' in row.get('class', []):
                continue
                
            cols = row.find_all('td')
            
            # Ensure the row has the expected number of data columns
            if len(cols) < 8:
                continue
                
            # Extract data mapping precisely to your HTML structure:
            # cols[0] = Favorite Icon (skip)
            # cols[1] = Rank Number
            # cols[2] = Name and Ticker
            # cols[3] = Earnings
            # cols[4] = Price
            # cols[5] = Daily Change
            # cols[6] = Sparkline Graph (skip)
            # cols[7] = Country
            
            rank = cols[1].text.strip()
            
            # Extract Company Name
            name_div = cols[2].find('div', class_='company-name')
            company_name = name_div.text.strip() if name_div else ""
            
            # Extract Ticker (and cleanly remove the embedded <span class="rank"> tag text)
            code_div = cols[2].find('div', class_='company-code')
            if code_div:
                rank_span = code_div.find('span', class_='rank')
                rank_span_text = rank_span.text if rank_span else ""
                ticker = code_div.text.replace(rank_span_text, "").strip()
            else:
                ticker = ""
                
            # Extract Earnings (Clean text string vs raw numeric value from 'data-sort')
            earnings_text = cols[3].text.strip().split(' ')[0] # e.g., "$195.68 B"
            raw_earnings = cols[3].get('data-sort', '')         # e.g., "195684000000"
            
            # Extract Stock Price
            stock_price = cols[4].text.strip()
            
            # Extract Country Name
            country = cols[7].text.strip()
            
            # Append organized dictionary data to our master list
            all_companies.append({
                'Rank': rank,
                'Company Name': company_name,
                'Ticker': ticker,
                'Earnings': earnings_text,
                'Raw Earnings ($)': raw_earnings,
                'Stock Price': stock_price,
                'Country': country
            })
            
        # Standard etiquette: wait 1 second between page hits to keep server traffic friendly
        time.sleep(1)
        
    except Exception as e:
        print(f"An unexpected error occurred on page {page}: {e}")
        break

# 3. Create a clean Dataframe layout using Pandas
df = pd.DataFrame(all_companies)

# 4. Save to CSV format
output_filename = 'companies_by_earnings.csv'
df.to_csv(output_filename, index=False)

print(f"\nSuccess! Extracted data for {len(df)} companies and saved to '{output_filename}'.")