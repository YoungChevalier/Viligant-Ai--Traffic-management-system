import os
import glob
import re

STATIC_DIR = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static"
html_files = glob.glob(os.path.join(STATIC_DIR, "*.html"))

# Regex to match the <li> containing violation-cases.html nav item
# Uses non-greedy .*? and re.DOTALL to match across lines
nav_regex = re.compile(r'\s*<li>\s*<a href="/static/violation-cases\.html" class="nav-item(?:\s+active)?">.*?</a>\s*</li>', re.DOTALL)

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content

    # 1. Remove from sidebar
    content = nav_regex.sub('', content)

    # 2. Update any buttons pointing to it (like the one in index.html)
    content = content.replace('href="/static/violation-cases.html" class="btn', 'href="/static/review-queue.html" class="btn')

    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(html_file)}")

# Delete the file itself
violation_file = os.path.join(STATIC_DIR, "violation-cases.html")
if os.path.exists(violation_file):
    os.remove(violation_file)
    print("Deleted violation-cases.html")
else:
    print("violation-cases.html not found")

