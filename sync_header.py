import os
import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_content = f.read()

    header_match = re.search(r'<header class="brutal-nav">.*?</header>', idx_content, re.DOTALL)
    if not header_match:
        print("Header not found in index.html")
        return
    
    header_raw = header_match.group(0)

    # Extract ticker
    ticker_match = re.search(r'<!-- Live Job Ticker -->.*?</div>\s*</div>', idx_content, re.DOTALL)
    ticker_raw = ticker_match.group(0) if ticker_match else ""

    # Make root version of header
    root_header = header_raw.replace('href="#home"', 'href="index.html#home"')
    root_header = root_header.replace('href="#latest-jobs"', 'href="index.html#latest-jobs"')
    root_header = root_header.replace('href="#admit-card"', 'href="index.html#admit-card"')
    root_header = root_header.replace('href="#result"', 'href="index.html#result"')
    root_header = root_header.replace('href="#answer-key"', 'href="index.html#answer-key"')
    root_header = root_header.replace('href="#syllabus"', 'href="index.html#syllabus"')
    root_header = root_header.replace('href="#admission"', 'href="index.html#admission"')
    root_header = root_header.replace('href="#documents"', 'href="index.html#documents"')

    # links_header for files in the /links/ folder
    links_header = root_header.replace('href="index.html', 'href="../index.html')

    # Update category.html
    with open('category.html', 'r', encoding='utf-8') as f:
        cat_content = f.read()
    
    if '<header' in cat_content:
        cat_content = re.sub(r'<header[^>]*>.*?</header>', root_header, cat_content, flags=re.DOTALL)
        # Update ticker in category.html
        if 'class="ticker-wrap"' in cat_content:
            cat_content = re.sub(r'<!-- Live Job Ticker -->.*?</div>\s*</div>', ticker_raw, cat_content, flags=re.DOTALL)
        else:
            cat_content = cat_content.replace(root_header, root_header + "\n\n" + ticker_raw)
            
        with open('category.html', 'w', encoding='utf-8') as f:
            f.write(cat_content)
        print("Updated category.html header and ticker.")

    # Update links/ files
    links_dir = './links'
    count = 0
    for filename in os.listdir(links_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(links_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '<header' in content:
                content = re.sub(r'<header[^>]*>.*?</header>', links_header, content, flags=re.DOTALL)
                
                # Update ticker in link files
                if 'class="ticker-wrap"' in content:
                    content = re.sub(r'<!-- Live Job Ticker -->.*?</div>\s*</div>', ticker_raw, content, flags=re.DOTALL)
                else:
                    content = content.replace(links_header, links_header + "\n\n" + ticker_raw)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                
    print(f"Updated header and ticker in {count} link files.")

if __name__ == '__main__':
    main()
