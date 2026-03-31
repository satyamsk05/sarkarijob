import os
import re

LINKS_DIR = 'links'
PROCESSED_COUNT = 0

# Template for dynamic meta description
TEMPLATE = 'Get the latest updates, result, admit card, and exam details for {title}. Sarkari Result Premium provides live notifications and free alerts.'

for filename in os.listdir(LINKS_DIR):
    if filename.endswith('.html'):
        filepath = os.path.join(LINKS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if description already exists to avoid duplication
        if '<meta name="description"' in content:
            continue
            
        # Extract title content
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            raw_title = title_match.group(1).strip()
            # Remove repeated "- Sarkari Result Premium" from raw_title if exists because it's already in our template sentence
            clean_title = raw_title.replace(' - Sarkari Result Premium', '').strip()
            
            description_text = TEMPLATE.format(title=clean_title)
            description_tag = f'\n    <meta name="description" content="{description_text}">'
            
            # Inject right below the title tag
            new_content = content.replace(f'<title>{raw_title}</title>', f'<title>{raw_title}</title>{description_tag}')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                PROCESSED_COUNT += 1

print(f"Successfully injected SEO metadata into {PROCESSED_COUNT} files.")
