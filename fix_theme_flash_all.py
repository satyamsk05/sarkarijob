import os
import re

LINKS_DIR = 'links'
CLEANUP_COUNT = 0

THEME_SCRIPT = """    <script>
        (function() {
            const savedTheme = localStorage.getItem('sarkari-theme') || 'light-theme';
            document.documentElement.className = savedTheme;
        })();
    </script>"""

for filename in os.listdir(LINKS_DIR):
    if filename.endswith('.html'):
        filepath = os.path.join(LINKS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Remove ANY existing theme script found in Head or Body
        # Using a more flexible regex to catch various indentations
        new_content = re.sub(r'\s*<script>\s*\(function\(\)\s*{\s*const\s+savedTheme\s*=\s*localStorage\.getItem\(\'sarkari-theme\'\)\s*\|\|\s*\'light-theme\';\s*document\.documentElement\.className\s*=\s*savedTheme;\s*}\)\(\);\s*</script>', '', content, flags=re.MULTILINE)
        
        # 2. Inject the clean script right at the top of the HEAD (after charset)
        if '<meta charset="UTF-8">' in new_content:
            new_content = new_content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + THEME_SCRIPT)
        elif '<head>' in new_content:
            new_content = new_content.replace('<head>', '<head>\n' + THEME_SCRIPT)

        # 3. Remove class="light-theme" from <body>
        new_content = new_content.replace('<body class="light-theme">', '<body>')

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            CLEANUP_COUNT += 1

print(f"Successfully optimized theme loading in {CLEANUP_COUNT} files.")
