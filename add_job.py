import json
import re
import os
import shutil

# Categories that exist in script.js
CATEGORIES = ['results', 'admitCard', 'latestJobs', 'answerKey', 'syllabus', 'admission']

def main():
    print("========================================")
    print(" Sarkari Job Payload Automator ")
    print("========================================\n")
    
    # 1. Gather User Input
    title = input("Enter Job Title (e.g., 'UP Police Constable Result'):\n> ").strip()
    
    print("\nSelect Category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")
        
    cat_idx = -1
    while cat_idx < 1 or cat_idx > len(CATEGORIES):
        try:
            cat_idx = int(input("> "))
        except ValueError:
            print("Please enter a valid number.")
            
    selected_category = CATEGORIES[cat_idx - 1]
    
    # Generate default URL slug
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    default_url = f"links/{slug}.html"
    
    print(f"\nGenerated default URL: {default_url}")
    url_input = input("Press ENTER to use default, or type a custom URL path:\n> ").strip()
    
    final_url = url_input if url_input else default_url
    
    # Optional HTML boilerplate copy
    html_prompt = input("\nDo you want to automatically create a blank template file at this URL? (Y/n):\n> ").strip().lower()
    
    if html_prompt != 'n':
        if not os.path.exists('links'):
            print("Error: 'links' directory not found. Skipping file creation.")
        else:
            # We will use category.html as a base structural proxy or empty html.
            if os.path.exists(final_url):
                print(f"File {final_url} already exists. Skipping creation.")
            else:
                try:
                    # Let's write a simple boilerplate
                    boilerplate = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Sarkari Result Premium</title>
    <!-- CSS and Header injected by sync_header.py logic -->
</head>
<body class="light-theme">
    <h1>{title}</h1>
    <!-- Footer injected by update_footer_all.py logic -->
</body>
</html>
'''
                    # Ensure path exists
                    os.makedirs(os.path.dirname(final_url) or '.', exist_ok=True)
                    with open(final_url, 'w', encoding='utf-8') as f:
                        f.write(boilerplate)
                    print(f"Created template at {final_url}")
                except Exception as e:
                    print(f"Could not create html boilerplate: {e}")
            
    # 2. Inject into script.js safely
    job_payload = {
        "title": title,
        "isNew": True,
        "originalUrl": final_url
    }
    
    # Format JSON payload properly with indentation
    payload_str = json.dumps(job_payload, indent=4)
    # Give it left padding
    payload_str = payload_str.replace('\n', '\n        ')
    
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            script_content = f.read()
            
        marker = f'"{selected_category}": ['
        if marker not in script_content:
            print(f"\nError: Could not find '{marker}' in script.js. Aborting.")
            return
            
        parts = script_content.split(marker, 1)
        
        # Inject right below
        injected_content = parts[0] + marker + '\n        ' + payload_str + ',\n' + parts[1].lstrip('\n ')
        
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(injected_content)
        
        print("\n[SUCCESS] Job payload successfully added to script.js!")
        
    except Exception as e:
        print(f"\nError modifying script.js: {e}")

if __name__ == "__main__":
    main()
