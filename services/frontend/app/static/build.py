import os
import re

static_dir = r'c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static'
index_path = os.path.join(static_dir, 'index.html')
settings_path = os.path.join(static_dir, 'settings.html')

with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

with open(settings_path, 'r', encoding='utf-8') as f:
    settings_content = f.read()

# Update navigation links in a content string
def update_nav(content):
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Dashboard</span>', r'<a href="/static/index.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg><span class="nav-text">Dashboard</span>', content, flags=re.DOTALL)
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Review Queue</span>', r'<a href="/static/review-queue.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg><span class="nav-text">Review Queue</span>', content, flags=re.DOTALL)
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Violation Cases</span>', r'<a href="/static/violation-cases.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg><span class="nav-text">Violation Cases</span>', content, flags=re.DOTALL)
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Search Records</span>', r'<a href="/static/search-records.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg><span class="nav-text">Search Records</span>', content, flags=re.DOTALL)
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Analytics</span>', r'<a href="/static/analytics.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg><span class="nav-text">Analytics</span>', content, flags=re.DOTALL)
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Cameras</span>', r'<a href="/static/cameras.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg><span class="nav-text">Cameras</span>', content, flags=re.DOTALL)
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Reviewers</span>', r'<a href="/static/reviewers.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg><span class="nav-text">Reviewers</span>', content, flags=re.DOTALL)
    content = re.sub(r'<a href="[^"]*"\s*class="nav-item(\s+active)?">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">Settings</span>', r'<a href="/static/settings.html" class="nav-item"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg><span class="nav-text">Settings</span>', content, flags=re.DOTALL)
    return content

def set_active(content, page_name):
    # Find the link block for page_name and replace nav-item with nav-item active
    def replacer(match):
        return match.group(0).replace('class="nav-item"', 'class="nav-item active"')
    
    return re.sub(r'<a href="[^"]*"\s*class="nav-item">\s*<svg[^>]*>.*?</svg>\s*<span class="nav-text">' + page_name + r'</span>', replacer, content, flags=re.DOTALL)

# Update index and settings
new_index = set_active(update_nav(index_content), 'Dashboard')
new_settings = set_active(update_nav(settings_content), 'Settings')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_index)

with open(settings_path, 'w', encoding='utf-8') as f:
    f.write(new_settings)

# Extract layout from updated index
start_idx = new_index.find('<!-- Breadcrumbs Row -->')
end_idx = new_index.find('</main>') + len('</main>')

header_part = new_index[:start_idx]
footer_part = new_index[end_idx:]

pages = [
    {'file': 'review-queue.html', 'name': 'Review Queue', 'subtitle': 'Manage and process pending traffic violation records.'},
    {'file': 'violation-cases.html', 'name': 'Violation Cases', 'subtitle': 'Browse and filter all generated violation cases.'},
    {'file': 'search-records.html', 'name': 'Search Records', 'subtitle': 'Search across plates, cases, and metadata logs.'},
    {'file': 'analytics.html', 'name': 'Analytics', 'subtitle': 'Performance metrics and system-wide analytics.'},
    {'file': 'cameras.html', 'name': 'Cameras', 'subtitle': 'Monitor and manage connected camera endpoints.'},
    {'file': 'reviewers.html', 'name': 'Reviewers', 'subtitle': 'Manage reviewer accounts and productivity.'}
]

for p in pages:
    base_shell = header_part
    base_shell = set_active(base_shell, p['name'])
    base_shell = base_shell.replace('<a href="/static/index.html" class="nav-item active">', '<a href="/static/index.html" class="nav-item">')
    
    content_area = f"""<!-- Breadcrumbs Row -->
                <div class="breadcrumbs-row">
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumbs">
                            <li class="breadcrumb-item"><a href="/static/index.html">Home</a></li>
                            <li class="breadcrumb-item active" aria-current="page">{p['name']}</li>
                        </ol>
                    </nav>
                </div>

                <!-- Main Content Area -->
                <main class="main-content">
                    
                    <!-- Page Title Area -->
                    <div class="page-title-area">
                        <div class="page-title-content">
                            <h1 class="page-title">{p['name']}</h1>
                            <p class="page-subtitle">{p['subtitle']}</p>
                        </div>
                    </div>

                    <!-- Placeholders Grid -->
                    <div class="content-placeholders">
                        <div class="card placeholder-block" style="padding: 40px; text-align: center; color: var(--color-text-muted);">
                            <p>Content for {p['name']} will be displayed here.</p>
                        </div>
                    </div>

                </main>"""
    
    full_html = base_shell + content_area + footer_part
    
    with open(os.path.join(static_dir, p['file']), 'w', encoding='utf-8') as f:
        f.write(full_html)

print("Success")
