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
});
