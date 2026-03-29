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

    # Make two versions of the header
    # 1. root_header for files in the root folder (like category.html)
    # Convert href="#..." to href="index.html#..."
    
    # We only want to replace href="# if it's not href="#" (the mobile menu or dropdown)
    root_header = header_raw.replace('href="#home"', 'href="index.html#home"')
    root_header = root_header.replace('href="#latest-jobs"', 'href="index.html#latest-jobs"')
    root_header = root_header.replace('href="#admit-card"', 'href="index.html#admit-card"')
    root_header = root_header.replace('href="#result"', 'href="index.html#result"')
    root_header = root_header.replace('href="#answer-key"', 'href="index.html#answer-key"')
    root_header = root_header.replace('href="#syllabus"', 'href="index.html#syllabus"')
    root_header = root_header.replace('href="#admission"', 'href="index.html#admission"')
    root_header = root_header.replace('href="#documents"', 'href="index.html#documents"')

    # 2. links_header for files in the /links/ folder
    links_header = root_header.replace('href="index.html', 'href="../index.html')

    # Update category.html
    with open('category.html', 'r', encoding='utf-8') as f:
        cat_content = f.read()
    
    if '<header' in cat_content:
        cat_content = re.sub(r'<header[^>]*>.*?</header>', root_header, cat_content, flags=re.DOTALL)
        with open('category.html', 'w', encoding='utf-8') as f:
            f.write(cat_content)
        print("Updated category.html header.")

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
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
            else:
                # Some files might not have a header, we can prepend it to body or main
                pass
                
    print(f"Updated header in {count} link files.")

if __name__ == '__main__':
    main()
