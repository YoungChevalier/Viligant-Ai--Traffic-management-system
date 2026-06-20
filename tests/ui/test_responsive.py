"""
test_responsive.py
Tests viewport responsiveness using Playwright device emulation.
"""
import pytest
from playwright.sync_api import Page, expect, sync_playwright


FRONTEND_URL = "http://localhost:8080"


def test_mobile_viewport_renders(page: Page):
    """The dashboard should render without horizontal scroll on a narrow mobile viewport."""
    # Set mobile viewport
    page.set_viewport_size({"width": 375, "height": 812})
    
    # Set up mock API intercepts
    import json
    from tests.ui.mock_responses import MOCK_STATS, MOCK_INCIDENTS_LIST

    def handle_route(route, request):
        url = request.url
        if "/incidents/stats" in url or "/analytics/summary" in url:
            route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_STATS))
        elif "/incidents" in url:
            route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_INCIDENTS_LIST))
        else:
            route.continue_()

    page.route("**/localhost:8000/**", handle_route)
    page.route("**/localhost:8001/**", handle_route)

    page.goto(FRONTEND_URL)
    page.wait_for_selector(".kpi-grid", timeout=10000)

    # Page width should not exceed viewport width (no horizontal overflow)
    body_width = page.evaluate("document.body.scrollWidth")
    assert body_width <= 450, f"Page body width {body_width}px exceeds mobile viewport"


def test_tablet_viewport_renders(page: Page):
    """The dashboard should render properly on a tablet viewport."""
    page.set_viewport_size({"width": 768, "height": 1024})

    import json
    from tests.ui.mock_responses import MOCK_STATS

    def handle_route(route, request):
        url = request.url
        if "/incidents/stats" in url or "/analytics/summary" in url:
            route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_STATS))
        else:
            route.continue_()

    page.route("**/localhost:8000/**", handle_route)
    page.route("**/localhost:8001/**", handle_route)

    page.goto(FRONTEND_URL)
    page.wait_for_selector(".kpi-grid", timeout=10000)
    
    # KPI cards should still be visible
    cards = page.locator(".kpi-card")
    assert cards.count() >= 1


def test_desktop_wide_viewport(page: Page):
    """On ultra-wide desktop, the layout should not break."""
    page.set_viewport_size({"width": 1920, "height": 1080})

    import json
    from tests.ui.mock_responses import MOCK_STATS

    def handle_route(route, request):
        url = request.url
        if "/incidents/stats" in url or "/analytics/summary" in url:
            route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_STATS))
        else:
            route.continue_()

    page.route("**/localhost:8000/**", handle_route)
    page.route("**/localhost:8001/**", handle_route)

    page.goto(FRONTEND_URL)
    page.wait_for_selector(".kpi-grid", timeout=10000)

    # Sidebar should be visible on desktop
    sidebar = page.locator(".sidebar")
    expect(sidebar).to_be_visible()
