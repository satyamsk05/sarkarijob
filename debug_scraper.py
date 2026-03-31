from detail_scraper import scrape_detail_page
import json

url = "https://www.sarkariresult.com/railway/rrb-alp-cen-01-2025/"
print(f"Debugging scraper on: {url}")
data = scrape_detail_page(url)
if data:
    print(json.dumps(data, indent=2))
else:
    print("Failed to scrape data")
