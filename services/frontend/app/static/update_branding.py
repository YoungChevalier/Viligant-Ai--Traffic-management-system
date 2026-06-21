import os
import glob

static_dir = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static"
html_files = glob.glob(os.path.join(static_dir, "*.html"))

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace title
    content = content.replace("<title>Traffic Violation Dashboard</title>", "<title>Vigilant AI</title>")
    
    # Replace logo text
    content = content.replace('<span class="logo-text">SentryTraffic</span>', '<span class="logo-text">Vigilant AI</span>')
    
    # Inject logo in header-right if not already there
    if 'src="/static/img/logo.png"' not in content:
        target = '<div class="header-right">'
        replacement = '<div class="header-right">\n                    <img src="/static/img/logo.png" alt="Vigilant AI" style="height: 32px; margin-right: 16px;">'
        content = content.replace(target, replacement)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Updated branding in {len(html_files)} HTML files.")
