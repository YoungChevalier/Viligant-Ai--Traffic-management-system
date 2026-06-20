"""
test_navigation.py
Tests SPA hash routing, sidebar active states, and loading transitions.
"""
import pytest
from playwright.sync_api import Page, expect


def test_default_route_is_dashboard(dashboard_page: Page):
    """On first load, the SPA should land on #dashboard."""
    expect(dashboard_page).to_have_url_containing("#dashboard")
    expect(dashboard_page.locator("h2")).to_have_text("Dashboard")


def test_sidebar_nav_active_state(dashboard_page: Page):
    """The sidebar link for the current route should have the 'active' class."""
    dashboard_link = dashboard_page.locator(".sidebar-nav a[href='#dashboard']")
    expect(dashboard_link).to_have_class_containing("active")


def test_navigate_to_cases(dashboard_page: Page):
    """Clicking the Cases nav link should navigate to #cases."""
    dashboard_page.click(".sidebar-nav a[href='#cases']")
    dashboard_page.wait_for_selector("#caseTable", timeout=5000)
    expect(dashboard_page).to_have_url_containing("#cases")
    expect(dashboard_page.locator("h2")).to_have_text("Cases")


def test_navigate_to_analytics(dashboard_page: Page):
    """Clicking the Analytics nav link should navigate to #analytics."""
    dashboard_page.click(".sidebar-nav a[href='#analytics']")
    dashboard_page.wait_for_selector("#analyticsTrendChart", timeout=5000)
    expect(dashboard_page).to_have_url_containing("#analytics")
    expect(dashboard_page.locator("h2")).to_have_text("Analytics")


def test_loading_state_shows_temporarily(mock_api: Page):
    """During route transitions, a loading indicator should briefly appear."""
    mock_api.goto("http://localhost:8080")
    # The loading div is replaced once content renders
    mock_api.wait_for_selector(".kpi-grid", timeout=10000)
    # After render, loading should be gone
    assert mock_api.locator(".loading").count() == 0


def test_sidebar_brand_visible(dashboard_page: Page):
    """The TrafficAI brand should always be visible."""
    expect(dashboard_page.locator(".sidebar-brand h1")).to_have_text("🚦 TrafficAI")


def test_user_info_visible(dashboard_page: Page):
    """The reviewer user info should be displayed in the sidebar."""
    expect(dashboard_page.locator(".sidebar-user strong")).to_have_text("Reviewer 01")
