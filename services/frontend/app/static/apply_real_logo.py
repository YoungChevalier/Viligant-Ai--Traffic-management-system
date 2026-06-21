import os
import glob
import re

static_dir = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static"
html_files = glob.glob(os.path.join(static_dir, "*.html"))

# The banana SVG
banana_svg_pattern = r'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#eab308" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logo-icon">.*?</svg>'

# The Vigilant AI Eye SVG
real_svg = """<svg width="24" height="24" viewBox="0 0 100 100" class="logo-icon" xmlns="http://www.w3.org/2000/svg">
  <path fill-rule="evenodd" clip-rule="evenodd" fill="currentColor" d="
    M 15 10 L 38 10 L 50 50 L 62 10 L 85 10 L 50 95 Z
    M 15 40 Q 50 15 85 40 Q 50 65 15 40 Z
    M 22 40 Q 50 22 78 40 Q 50 58 22 40 Z
    M 26 40 Q 50 28 74 40 Q 50 52 26 40 Z
    M 50 32 A 8 8 0 1 0 50 48 A 8 8 0 1 0 50 32 Z
    M 53 35 A 2 2 0 1 1 53 39 A 2 2 0 1 1 53 35 Z
  " />
</svg>"""

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace Banana SVG with Real SVG
    content = re.sub(banana_svg_pattern, real_svg, content, flags=re.DOTALL)
    
    # Just to be absolutely thorough on the branding text in case any variant exists
    content = content.replace("Traffic Manager", "Vigilant AI")
    content = content.replace("SentryTraffic", "Vigilant AI")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Applied the real Vigilant AI SVG to {len(html_files)} files.")
