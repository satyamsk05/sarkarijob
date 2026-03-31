import os
import re
import json
import subprocess
from scraper import scrape_sarkari_result
from detail_scraper import scrape_detail_page

SCRIPT_JS = 'script.js'
LINKS_DIR = 'links'
CATEGORIES = ['results', 'admitCard', 'latestJobs']

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def run_sync_scripts():
    scripts = [
        'sync_header.py',
        'update_footer_all.py',
        'inject_seo.py',
        'fix_theme_flash_all.py',
        'sync_search_overlay.py'
    ]
    print("\n--- Running Sync Suite for New Look ---")
    for script in scripts:
        if os.path.exists(script):
            print(f"Executing {script}...")
            subprocess.run(['python3', script], capture_output=True)
    print("--- Sync Suite Completed ---\n")

def generate_rich_html(title, original_url, data):
    if not data:
        data = {
            "title": title,
            "short_info": "Detailed information for this post will be updated shortly.",
            "important_dates": ["Check official notification"],
            "application_fee": ["Check official notification"],
            "age_limit": "Refer notification",
            "vacancy_details": [],
            "links": [{"text": "Official Website", "url": original_url}]
        }

    dates_html = "".join([f"<li>{item}</li>" for item in data.get('important_dates', [])])
    fees_html = "".join([f"<li>{item}</li>" for item in data.get('application_fee', [])])
    
    # Vacancy Table Logic
    vacancy_html = ""
    if data.get('vacancy_details'):
        rows_html = ""
        for i, row in enumerate(data['vacancy_details']):
            is_header = i == 0 and ("post" in row[0].lower() or "vacancy" in row[0].lower())
            tag = "th" if is_header else "td"
            cells = "".join([f"<{tag}>{c}</{tag}>" for c in row])
            rows_html += f"<tr>{cells}</tr>"
        
        vacancy_html = f'''
        <div class="vacancy-section">
            <div class="vacancy-header">
                <h3><i class="ph ph-users-four"></i> Vacancy Details & Eligibility</h3>
            </div>
            <div class="rich-table-wrapper">
                <table class="rich-table">
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>'''

    links_rows = "".join([
        f'<tr><td>{link["text"]}</td><td><a href="{link["url"]}" class="btn-link" target="_blank">Click Here <i class="ph ph-arrow-square-out"></i></a></td></tr>'
        for link in data.get('links', [])
    ])

    summary_html = f'''
    <div class="summary-box">
        <div class="summary-text">
            {data.get('short_info', 'Information summary loading...')}
        </div>
    </div>''' if data.get('short_info') else ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Sarkari Result 2026</title>
    <link rel="stylesheet" href="../style.css">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="../script.js"></script>
</head>
<body class="light-theme">
    <header class="brutal-nav"></header>
    
    <!-- Live Job Ticker -->
    <div class="ticker-wrap">
        <div class="ticker-label">
            <div class="pulse-dot"></div> SARKARI LIVE
        </div>
        <div class="ticker" id="live-ticker"></div>
    </div>
    
    <main class="detail-container">
        <div class="detail-header">
            <h1 class="detail-title">{title}</h1>
            <div class="detail-meta">
                <span><i class="ph ph-calendar"></i> Updated: 2026</span>
                <span><i class="ph ph-shield-check"></i> Verified by Sarkari Job</span>
            </div>
        </div>

        {summary_html}

        <div class="info-grid">
            <div class="info-card">
                <h3><i class="ph ph-calendar-check"></i> Important Dates</h3>
                <ul class="info-list">
                    {dates_html}
                </ul>
            </div>
            <div class="info-card">
                <h3><i class="ph ph-currency-circle-dollar"></i> Application Fee</h3>
                <ul class="info-list">
                    {fees_html}
                </ul>
            </div>
        </div>

        <div class="requirement-section">
            <h3><i class="ph ph-user-focus"></i> Age Limit & Requirements</h3>
            <div style="margin-top: 20px;">
                <p>{data.get('age_limit', 'Refer notification')}</p>
            </div>
        </div>

        {vacancy_html}

        <div class="links-table-container">
            <table class="links-table">
                <thead>
                    <tr>
                        <th>Action / Link Description</th>
                        <th>Resource</th>
                    </tr>
                </thead>
                <tbody>
                    {links_rows}
                </tbody>
            </table>
        </div>

        <div style="margin-top: 40px; text-align: center; color: var(--text-muted);">
            <p>Full content extracted from official source | Redesigned for Sarkari Job</p>
        </div>
    </main>

    <footer class="brutal-footer"></footer>
</body>
</html>'''

def main():
    print("🚀 Starting Full Content Scraper & Rich Rollout...")
    
    scraped_items = scrape_sarkari_result()
    if not scraped_items:
        print("❌ No items scraped. Aborting.")
        return

    print(f"🔎 Found {len(scraped_items)} items on Sarkari Result.")

    with open(SCRIPT_JS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_items_count = 0
    generated_files = []

    for item in scraped_items:
        category = item['category']
        title = item['title']
        original_url = item['originalUrl']
        
        slug = slugify(title)
        local_url = f"links/{slug}.html"
        
        needs_deep_scrape = False
        if not os.path.exists(local_url):
            needs_deep_scrape = True
        else:
            with open(local_url, 'r', encoding='utf-8') as f_check:
                file_content = f_check.read()
                # If "summary-box" is missing, we force an update for v5.1 "full content"
                if 'summary-box' not in file_content:
                    needs_deep_scrape = True

        if needs_deep_scrape:
            print(f"📦 Full Scraping: {title}...")
            detail_data = scrape_detail_page(original_url)
            
            try:
                rich_html = generate_rich_html(title, original_url, detail_data)
                os.makedirs(os.path.dirname(local_url), exist_ok=True)
                with open(local_url, 'w', encoding='utf-8') as f_out:
                    f_out.write(rich_html)
                generated_files.append(local_url)
            except Exception as e:
                print(f"⚠️ Failed to update {local_url}: {e}")

        # Inject into script.js only if NOT already there
        if f'"{title}"' not in content and f"'{title}'" not in content:
            marker = f'"{category}": ['
            if marker in content:
                job_payload = {
                    "title": title,
                    "isNew": True,
                    "originalUrl": local_url
                }
                payload_str = json.dumps(job_payload, indent=8).strip('{}')
                payload_str = "        {" + payload_str + "        }"
                
                parts = content.split(marker, 1)
                content = parts[0] + marker + '\n' + payload_str + ',\n' + parts[1].lstrip('\n ')
                new_items_count += 1

    if new_items_count > 0:
        with open(SCRIPT_JS, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully added {new_items_count} new items to script.js.")
        
    if generated_files:
        print(f"📝 Generated/Updated {len(generated_files)} FULL CONTENT HTML files.")
        run_sync_scripts()
    else:
        print("✨ No new items found. Everything is up to date!")

if __name__ == "__main__":
    main()
