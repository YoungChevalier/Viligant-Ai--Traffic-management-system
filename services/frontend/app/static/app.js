/**
 * Traffic Violation Dashboard - Shell UI Behaviors
 */

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileCloseBtn = document.getElementById('mobileCloseBtn');
    const themeToggleBtn = document.getElementById('themeToggle');
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationDropdown = document.getElementById('notificationDropdown');
    const userProfileBtn = document.getElementById('userProfileBtn');
    const userDropdown = document.getElementById('userDropdown');

    // State
    let isSidebarOpen = false;

    // --- Sidebar Mobile Drawer ---
    const toggleSidebar = () => {
        isSidebarOpen = !isSidebarOpen;
        if (isSidebarOpen) {
            sidebar.classList.add('drawer-open');
            sidebarOverlay.classList.add('active');
            sidebarToggle.setAttribute('aria-expanded', 'true');
            sidebarOverlay.setAttribute('aria-hidden', 'false');
        } else {
            sidebar.classList.remove('drawer-open');
            sidebarOverlay.classList.remove('active');
            sidebarToggle.setAttribute('aria-expanded', 'false');
            sidebarOverlay.setAttribute('aria-hidden', 'true');
        }
    };

    if (sidebarToggle) sidebarToggle.addEventListener('click', toggleSidebar);
    if (mobileCloseBtn) mobileCloseBtn.addEventListener('click', toggleSidebar);
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', toggleSidebar);

    // --- Theme Toggle ---
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('dashboard-theme', theme);
    };

    // Initialize Theme
    const savedTheme = localStorage.getItem('dashboard-theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        // Check OS preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark ? 'dark' : 'light');
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            setTheme(currentTheme === 'light' ? 'dark' : 'light');
        });
    }

    // --- Dropdown Management ---
    const closeAllDropdowns = () => {
        const dropdowns = [
            { menu: notificationDropdown, btn: notificationBtn },
            { menu: userDropdown, btn: userProfileBtn }
        ];

        dropdowns.forEach(({ menu, btn }) => {
            if (menu && menu.classList.contains('show')) {
                menu.classList.remove('show');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            }
        });
    };

    const toggleDropdown = (e, menu, btn) => {
        e.stopPropagation(); // Prevent document click from immediately closing
        
        const isShowing = menu.classList.contains('show');
        
        // Close others first
        closeAllDropdowns();
        
        if (!isShowing) {
            menu.classList.add('show');
            btn.setAttribute('aria-expanded', 'true');
        }
    };

    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', (e) => toggleDropdown(e, notificationDropdown, notificationBtn));
    }

    if (userProfileBtn && userDropdown) {
        userProfileBtn.addEventListener('click', (e) => toggleDropdown(e, userDropdown, userProfileBtn));
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (
            (notificationDropdown && notificationDropdown.classList.contains('show') && !notificationDropdown.contains(e.target)) ||
            (userDropdown && userDropdown.classList.contains('show') && !userDropdown.contains(e.target))
        ) {
            closeAllDropdowns();
        }
    });

    // Close dropdowns on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllDropdowns();
            
            // Also close sidebar on escape if open
            if (isSidebarOpen) toggleSidebar();
        }
    });

    // Dashboard refresh
    const refreshBtn = document.getElementById('refreshDashboardBtn');
    if (refreshBtn && typeof window.refreshDashboard === 'function') {
        refreshBtn.addEventListener('click', () => window.refreshDashboard());
    }

    // --- Global Search Suggestions ---
    const searchInput = document.querySelector('.search-input');
    const searchSuggestions = document.getElementById('globalSearchSuggestions');

    if (searchInput && searchSuggestions) {
        // Mock data pool
        const suggestionPool = [
            { type: 'Plate', title: 'ABC-1234', subtitle: 'Speeding Violation' },
            { type: 'Plate', title: 'XYZ-9876', subtitle: 'Red Light' },
            { type: 'Case', title: 'CASE-2023-010', subtitle: 'Pending Review' },
            { type: 'Case', title: 'CASE-2023-011', subtitle: 'Approved' },
            { type: 'Camera', title: 'CAM-NORTH-01', subtitle: 'Intersection 5' },
            { type: 'Camera', title: 'CAM-EAST-04', subtitle: 'Highway 9' },
            { type: 'Plate', title: 'DEF-5566', subtitle: 'Illegal Parking' },
        ];

        let searchTimeout = null;

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            
            if (searchTimeout) clearTimeout(searchTimeout);
            
            if (query.length === 0) {
                searchSuggestions.style.display = 'none';
                return;
            }

            searchTimeout = setTimeout(() => {
                const results = suggestionPool.filter(item => 
                    item.title.toLowerCase().includes(query) || 
                    item.subtitle.toLowerCase().includes(query) ||
                    item.type.toLowerCase().includes(query)
                );

                if (results.length > 0) {
                    searchSuggestions.innerHTML = results.map(r => `
                        <div class="suggestion-item" onclick="window.location.href='#'">
                            <div class="suggestion-icon">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                            </div>
                            <div class="suggestion-content">
                                <div class="suggestion-title">${r.title}</div>
                                <div class="suggestion-subtitle">${r.type} &bull; ${r.subtitle}</div>
                            </div>
                        </div>
                    `).join('');
                    searchSuggestions.style.display = 'block';
                } else {
                    searchSuggestions.innerHTML = `
                        <div class="suggestion-item" style="cursor: default; justify-content: center; color: var(--text-muted);">
                            No results found
                        </div>
                    `;
                    searchSuggestions.style.display = 'block';
                }
            }, 300); // 300ms debounce
        });

        // Hide when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
                searchSuggestions.style.display = 'none';
            }
        });
        
        // Show on focus if there's text
        searchInput.addEventListener('focus', (e) => {
            if (e.target.value.trim().length > 0 && searchSuggestions.innerHTML.trim() !== '') {
                searchSuggestions.style.display = 'block';
            }
        });
    }
});

