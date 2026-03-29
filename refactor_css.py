import codecs

with codecs.open('style.css', 'r', 'utf-8') as f:
    css = f.read()

# Replace :root { ... }
root_original = """:root {
    --primary: #22c55e;
    --primary-dark: #16a34a;
    --secondary: #a5f3fc;
    --accent-pink: #f43f5e;
    --accent-yellow: #fbbf24;
    --bg-main: #f8fafc;
    --text-main: #0f172a;
    --border-color: #0f172a;
    --border-width: 3px;
    --shadow-offset: 5px;
    --shadow-offset-hover: 8px;
    --header-height: 80px;
    --transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}"""

root_new = """:root {
    --primary: #22c55e;
    --primary-dark: #16a34a;
    --secondary: #a5f3fc;
    --accent-pink: #f43f5e;
    --accent-yellow: #fbbf24;
    --bg-main: #f8fafc;
    --card-bg: #ffffff;
    --text-main: #0f172a;
    --border-color: #0f172a;
    --footer-bg: #0f172a;
    --footer-text: #ffffff;
    --border-width: 3px;
    --shadow-offset: 5px;
    --shadow-offset-hover: 8px;
    --header-height: 80px;
    --transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}"""

css = css.replace(root_original, root_new)

# Replace .dark-theme { ... }
dark_original = """.dark-theme {
    --bg-main: #131313;
    --text-main: #ffffff;
    --border-color: #ffffff;
    --primary: #4ade80;
    --secondary: #22d3ee;
}"""

dark_new = """.dark-theme {
    --bg-main: #131313;
    --card-bg: #1e1e1e;
    --text-main: #ffffff;
    --border-color: #ffffff;
    --footer-bg: #1e1e1e;
    --footer-text: #ffffff;
    --primary: #4ade80;
    --secondary: #f43f5e;
}"""

css = css.replace(dark_original, dark_new)

# Replace all background: white; with background: var(--card-bg);
css = css.replace('background: white;', 'background: var(--card-bg);')

# Replace .brutal-footer colors
footer_original = """.brutal-footer {
    margin-top: 8rem;
    padding: 6rem 0 3rem;
    background: var(--border-color);
    color: white;"""

footer_new = """.brutal-footer {
    margin-top: 8rem;
    padding: 6rem 0 3rem;
    background: var(--footer-bg);
    color: var(--footer-text);"""

css = css.replace(footer_original, footer_new)

# Add fallback replacement if footer didn't match perfectly
if footer_new not in css:
    css = css.replace('background: var(--border-color);\n    color: white;', 'background: var(--footer-bg);\n    color: var(--footer-text);')

# Small fix for dark mode inputs and things
# Let's ensure input backgrounds look good in both modes
input_org = """.subscribe-group input {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.3);"""

input_new = """.subscribe-group input {
    background: var(--bg-main);
    border: 2px solid var(--border-color);"""
css = css.replace(input_org, input_new)

with codecs.open('style.css', 'w', 'utf-8') as f:
    f.write(css)

print("CSS variables and dark mode updated successfully.")
