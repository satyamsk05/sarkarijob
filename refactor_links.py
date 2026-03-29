import os
import re

def refactor_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace classes
    content = content.replace('glass-nav', 'brutal-nav')
    content = content.replace('glass-footer', 'brutal-footer')
    content = content.replace('info-card glass', 'info-card brutal-card')
    content = content.replace('sarkari-content glass', 'sarkari-content brutal-card')
    content = content.replace('whatsapp-card glass', 'whatsapp-card brutal-card')
    
    # Add brutal-table class to tables
    content = content.replace('<table', '<table class="brutal-table"')
    # Remove duplicate class if it already had one
    content = content.replace('class="brutal-table" class="', 'class="brutal-table ')
    
    # Update internal styles if present (specifically table and glass references)
    content = content.replace('var(--glass-bg)', '#ffffff')
    content = content.replace('var(--glass-border)', 'var(--border-color)')
    content = content.replace('var(--glass-shadow)', '5px 5px 0px var(--border-color)')
    
    # Remove blobs if any
    content = re.sub(r'<div class="blob-container">.*?</div>', '', content, flags=re.DOTALL)
    
    # Fix inline styles for info-card to match index.html
    content = content.replace('border-radius: 25px;', 'border-radius: 20px;')
    content = content.replace('border-radius: 16px;', 'border-radius: 20px;')
    content = content.replace('border-radius: 12px;', 'border-radius: 20px;')
    
    # Update title styling in info-card
    content = content.replace('color: var(--primary); font-size: 2.2rem;', 'color: var(--text-main); font-size: 2.5rem; font-weight: 900; text-transform: uppercase;')
    content = content.replace('color: var(--primary); font-size: 1.8rem;', 'color: var(--text-main); font-size: 2.2rem; font-weight: 900; text-transform: uppercase;')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    links_dir = './links'
    for filename in os.listdir(links_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(links_dir, filename)
            print(f"Refactoring {filepath}...")
            refactor_file(filepath)
    
    # Also refactor index.html and category.html if needed (though already done mostly)
    # but good for consistency check.
    # refactor_file('index.html')
    # refactor_file('category.html')

if __name__ == "__main__":
    main()
