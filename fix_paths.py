import os
import glob

static_dir = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static"

files_to_check = glob.glob(os.path.join(static_dir, "*.html")) + glob.glob(os.path.join(static_dir, "*.js"))

for filepath in files_to_check:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace /static/ with relative paths
    if "/static/" in content:
        new_content = content.replace('href="/static/', 'href="./')
        new_content = new_content.replace("href='/static/", "href='./")
        new_content = new_content.replace('src="/static/', 'src="./')
        new_content = new_content.replace("src='/static/", "src='./")
        new_content = new_content.replace('"/static/login.html"', '"./login.html"')
        
        # Only rewrite if there was actually a change
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated paths in {os.path.basename(filepath)}")
