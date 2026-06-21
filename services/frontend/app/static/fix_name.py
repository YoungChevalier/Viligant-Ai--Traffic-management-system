import os
import glob
import re

static_dir = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static"
html_files = glob.glob(os.path.join(static_dir, "*.html"))

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace TrafficManager (no space)
    content = content.replace("TrafficManager", "Vigilant AI")
    # Replace Traffic Manager (with space)
    content = content.replace("Traffic Manager", "Vigilant AI")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Fixed 'TrafficManager' in {len(html_files)} files.")
