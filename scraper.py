import requests
from bs4 import BeautifulSoup
import re

def scrape_sarkari_result():
    url = "https://www.sarkariresult.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Mapping our internal category keys to the display text on the site
    mapping = {
        "results": "Result",
        "admitCard": "Admit Card",
        "latestJobs": "Latest Job"
    }

    scraped_data = []

    # Find all divs that might be headers
    # Based on curl, headers are in divs with align="center" inside div#heading
    all_headers = soup.find_all('div', id='heading')
    
    for category_key, search_text in mapping.items():
        target_heading = None
        for h in all_headers:
            if search_text.lower() in h.get_text().lower():
                target_heading = h
                break
        
        if target_heading:
            # The next sibling div with id="post" contains the links
            post_div = target_heading.find_next_sibling('div', id='post')
            if not post_div:
                # Try parent's sibling if structure is different
                post_div = target_heading.parent.find('div', id='post')

            if post_div:
                links = post_div.find_all('li')
                for li in links:
                    a = li.find('a')
                    if a:
                        title = a.get_text().strip()
                        href = a.get('href', '').strip()
                        
                        if title and href:
                            # Standardize URL
                            if href.startswith('//'):
                                href = 'https:' + href
                            elif href.startswith('/'):
                                href = 'https://www.sarkariresult.com' + href

                            scraped_data.append({
                                "category": category_key,
                                "title": title,
                                "originalUrl": href,
                                "isNew": "new" in li.get_text().lower() or "new" in a.get_text().lower()
                            })

    return scraped_data

if __name__ == "__main__":
    data = scrape_sarkari_result()
    print(f"Scraped {len(data)} items.")
    for item in data[:10]:
        print(f"[{item['category']}] {item['title']} -> {item['originalUrl']}")
