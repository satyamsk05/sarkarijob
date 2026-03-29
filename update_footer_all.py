import os
import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_content = f.read()

    footer_match = re.search(r'<footer class="brutal-footer">.*?</footer>', idx_content, re.DOTALL)
    if not footer_match:
        print("Footer not found in index.html")
        return
    
    new_footer_raw = footer_match.group(0)

    # Adjust paths for relative location in /links/
    new_footer_links = new_footer_raw.replace('links/', '')
    new_footer_links = new_footer_links.replace('"category.html', '"../category.html')
    new_footer_links = new_footer_links.replace('"index.html', '"../index.html')

    links_dir = './links'
    count = 0
    for filename in os.listdir(links_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(links_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '<footer' in content:
                content = re.sub(r'<footer[^>]*>.*?</footer>', new_footer_links, content, flags=re.DOTALL)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
    print(f"Updated footer in {count} files.")

if __name__ == '__main__':
    main()
