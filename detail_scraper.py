import requests
from bs4 import BeautifulSoup
import re

def scrape_detail_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching detail {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = {
        "title": "",
        "short_info": "",
        "important_dates": [],
        "application_fee": [],
        "age_limit": "",
        "eligibility": "",
        "vacancy_details": [],
        "links": []
    }

    title_h1 = soup.find('h1')
    if title_h1:
        data["title"] = title_h1.get_text().strip()

    # 1. Broad Search for Short Info (Anywhere in document)
    for row in soup.find_all('tr'):
        row_text = row.get_text().replace('\xa0', ' ').strip()
        if re.search(r'short\s+information', row_text.lower()):
            clean_info = re.sub(r'short\s+information\s*:?', '', row_text, flags=re.IGNORECASE).strip()
            if clean_info:
                data["short_info"] = clean_info
                break

    # 2. Identify the TRUE content table by looking for "Important Dates"
    main_table = None
    all_tables = soup.find_all('table')
    for table in all_tables:
        if "important dates" in table.get_text().lower():
            main_table = table
            # On some pages, there are multiple tables. We want the one with most rows.
            
    if not main_table:
        return data # Return partial data if main table missing

    # Get all rows in the content area
    rows = main_table.find_all('tr')
    
    mode = "META"
    
    for row in rows:
        cells = row.find_all('td', recursive=False)
        if not cells: continue
        
        row_text = row.get_text().replace('\xa0', ' ').strip()
        text_lower = row_text.lower()
        
        # --- Mode Switches ---
        if re.search(r'important\s+dates|application\s+fee', text_lower):
            mode = "META"
        
        if re.search(r'post\s+name|vacancy\s+details|eligibility', text_lower):
            if mode != "LINKS" and len(row_text) < 300:
                mode = "VACANCY"

        if re.search(r'important\s+links|useful\s+links', text_lower):
            mode = "LINKS"
            continue

        # --- Extraction ---
        if mode == "META":
            for cell in cells:
                c_text = cell.get_text().replace('\xa0', ' ').strip()
                c_lower = c_text.lower()
                if "important dates" in c_lower:
                    data["important_dates"] = [li.strip() for li in c_text.split('\n') if li.strip() and "important dates" not in li.lower()]
                elif "application fee" in c_lower:
                    data["application_fee"] = [li.strip() for li in c_text.split('\n') if li.strip() and "application fee" not in li.lower()]
                elif "age limit" in c_lower:
                    data["age_limit"] = c_text

        elif mode == "VACANCY":
            if re.search(r'android\s+apps|apple\s+ios|telegram|whatsapp|click\s+here', text_lower):
                continue
            
            row_data = [c.get_text().strip() for c in cells if c.get_text().strip()]
            if len(row_data) >= 2:
                if not re.search(r'important\s+dates|application\s+fee', text_lower):
                    data["vacancy_details"].append(row_data)

        elif mode == "LINKS":
            for a in row.find_all('a'):
                l_text = a.get_text().strip()
                l_href = a.get('href', '').strip()
                if l_text and l_href:
                    if l_href.startswith('/'): l_href = "https://www.sarkariresult.com" + l_href
                    data["links"].append({"text": l_text, "url": l_href})

    return data

if __name__ == "__main__":
    test_url = "https://www.sarkariresult.com/2026/uptet-2026/"
    print(f"Testing deep scraper on {test_url}")
    res = scrape_detail_page(test_url)
    if res:
        print(f"Title: {res['title']}")
        print(f"Short Info: {res['short_info'][:100]}...")
        print(f"Vacancy Rows: {len(res['vacancy_details'])}")
        print(f"Links found: {len(res['links'])}")
