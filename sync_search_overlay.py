import os

LINKS_DIR = 'links'
SYNC_COUNT = 0

OVERLAY_HTML = """    <!-- Premium Search Overlay -->
    <div id="search-overlay" class="search-overlay">
        <div class="overlay-content">
            <div class="search-header">
                <div class="search-input-wrapper">
                    <i class="ph ph-magnifying-glass"></i>
                    <input type="text" id="overlay-search-input" placeholder="Search for jobs, admit cards, results..." autocomplete="off">
                </div>
                <button id="close-search" class="close-btn">
                    <i class="ph ph-x"></i>
                    <span>CLOSE</span>
                </button>
            </div>
            
            <div id="search-results-container" class="search-results-container">
                <!-- Search results will be populated here -->
                <div class="search-placeholder">
                    <i class="ph ph-sparkle"></i>
                    <p>Start typing to discover latest updates...</p>
                </div>
            </div>
        </div>
    </div>
"""

for filename in os.listdir(LINKS_DIR):
    if filename.endswith('.html'):
        filepath = os.path.join(LINKS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'id="search-overlay"' in content:
            continue

        if '</body>' in content:
            new_content = content.replace('</body>', OVERLAY_HTML + '</body>')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                SYNC_COUNT += 1

print(f"Successfully synced Search Overlay into {SYNC_COUNT} files.")
