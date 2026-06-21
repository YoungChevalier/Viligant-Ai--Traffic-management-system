import os
import glob
import re

static_dir = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static"
html_files = glob.glob(os.path.join(static_dir, "*.html"))

# The old SVG
old_svg_pattern = r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logo-icon">.*?</svg>'

# Banana SVG
banana_svg = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#eab308" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logo-icon"><path d="M4 13c1.5-6 9-7 15-2 1 1 2 3 2 5-6-3-12-3-17 0-1-1-1-2 0-3z"></path><path d="M19 11c-2-2-5-3-8-2"></path></svg>'

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace old SVG with Banana SVG
    content = re.sub(old_svg_pattern, banana_svg, content, flags=re.DOTALL)
    
    # Just in case "Traffic Manager" is somewhere
    content = content.replace("Traffic Manager", "Vigilant AI")
    content = content.replace("traffic manager", "Vigilant AI")
    content = content.replace("Traffic manager", "Vigilant AI")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Updated logo to a Nano Banana in {len(html_files)} files.")
