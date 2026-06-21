import os
import glob
import re

STATIC_DIR = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static"

html_files = glob.glob(os.path.join(STATIC_DIR, "*.html"))

# We want to add the Alerts Center link right before the settings link.
# We also want to map URLs to filenames for active state replacement.

ALERTS_NAV_HTML = """                    <li>
                        <a href="/static/alerts.html" class="nav-item{alerts_active}">
                            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                            <span class="nav-text">Alerts Center</span>
                        </a>
                    </li>
"""

# Regex to find the <ul> containing settings
# Actually, the sidebar divider looks like:
#                 <div class="nav-section-divider"></div>
#                 
#                 <ul>
#                     <li>
#                         <a href="/static/settings.html"

def inject_alerts_nav(content, current_filename):
    # Check if alerts is already in there
    if 'href="/static/alerts.html"' in content:
        # Just update active state
        return content

    # Add the alerts nav item
    alerts_html = ALERTS_NAV_HTML.format(alerts_active=" active" if current_filename == "alerts.html" else "")
    
    target_block = """                <div class="nav-section-divider"></div>
                
                <ul>"""
    
    if target_block in content:
        return content.replace(target_block, target_block + "\n" + alerts_html)
    return content

def fix_active_state(content, current_filename):
    # Remove ' active' from all nav-items
    content = re.sub(r'class="nav-item active"', r'class="nav-item"', content)
    
    # Add ' active' to the current one
    # We look for <a href="/static/filename" class="nav-item"
    target_href = f'href="/static/{current_filename}" class="nav-item"'
    if target_href in content:
        content = content.replace(target_href, f'href="/static/{current_filename}" class="nav-item active"')
    else:
        # handle index.html which maps to Dashboard
        if current_filename == "index.html":
            target_href = f'href="/static/index.html" class="nav-item"'
            if target_href in content:
                content = content.replace(target_href, f'href="/static/index.html" class="nav-item active"')

    return content

def fix_view_history_link(content):
    # Replace <button class="btn-link">View All History</button> 
    # Or <a href="#" class="btn-link">View All History</a>
    # With <a href="/static/alerts.html" class="btn-link" style="display:block; text-align:center;">View All History</a>
    
    # First, try to replace button if it exists
    content = re.sub(
        r'<button class="btn-link"[^>]*>View All History</button>',
        r'<a href="/static/alerts.html" class="btn-link" style="display:inline-block; width:100%; text-align:center;">View All History</a>',
        content
    )
    
    # Also if it's already an 'a' tag but with href="#"
    content = re.sub(
        r'<a href="#" class="btn-link"[^>]*>View All History</a>',
        r'<a href="/static/alerts.html" class="btn-link" style="display:inline-block; width:100%; text-align:center;">View All History</a>',
        content
    )
    
    return content


for html_file in html_files:
    filename = os.path.basename(html_file)
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject alerts nav
    content = inject_alerts_nav(content, filename)
    
    # 2. Fix active state
    content = fix_active_state(content, filename)
    
    # 3. Fix View All History
    content = fix_view_history_link(content)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Navigation finalized across {len(html_files)} files.")
