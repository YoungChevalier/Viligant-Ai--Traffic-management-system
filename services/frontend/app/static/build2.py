import os

static_dir = r'c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static'
index_path = os.path.join(static_dir, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    base_html = f.read()

# Pages configuration
pages = [
    {'file': 'review-queue.html', 'name': 'Review Queue', 'subtitle': 'Manage and process pending traffic violation records.', 'nav_text': 'Review Queue'},
    {'file': 'violation-cases.html', 'name': 'Violation Cases', 'subtitle': 'Browse and filter all generated violation cases.', 'nav_text': 'Violation Cases'},
    {'file': 'search-records.html', 'name': 'Search Records', 'subtitle': 'Search across plates, cases, and metadata logs.', 'nav_text': 'Search Records'},
    {'file': 'analytics.html', 'name': 'Analytics', 'subtitle': 'Performance metrics and system-wide analytics.', 'nav_text': 'Analytics'},
    {'file': 'cameras.html', 'name': 'Cameras', 'subtitle': 'Monitor and manage connected camera endpoints.', 'nav_text': 'Cameras'},
    {'file': 'reviewers.html', 'name': 'Reviewers', 'subtitle': 'Manage reviewer accounts and productivity.', 'nav_text': 'Reviewers'}
]

# We want to replace the Dashboard active class to inactive
base_html = base_html.replace('class="nav-item active"', 'class="nav-item"')

def get_content_area(p):
    return f"""<!-- Breadcrumbs Row -->
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

for p in pages:
    # 1. Update the nav item to be active
    # We find the specific href for this page and make it active
    target_href = f'href="/static/{p["file"]}" class="nav-item"'
    new_href = f'href="/static/{p["file"]}" class="nav-item active"'
    page_html = base_html.replace(target_href, new_href)
    
    # 2. Replace the main content area
    # We'll split at <!-- Breadcrumbs Row --> and </main>
    start_idx = page_html.find('<!-- Breadcrumbs Row -->')
    end_idx = page_html.find('</main>') + len('</main>')
    
    if start_idx != -1 and end_idx != -1:
        header_part = page_html[:start_idx]
        footer_part = page_html[end_idx:]
        
        full_html = header_part + get_content_area(p) + footer_part
        
        with open(os.path.join(static_dir, p['file']), 'w', encoding='utf-8') as f:
            f.write(full_html)

print("Done generating new pages")
