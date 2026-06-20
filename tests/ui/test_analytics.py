"""
test_analytics.py
Tests for the #analytics view: chart canvases, KPI consistency, filters, refresh.
"""
import pytest
from playwright.sync_api import Page, expect


def _go_to_analytics(page: Page):
    page.click(".sidebar-nav a[href='#analytics']")
    page.wait_for_selector("#analyticsTrendChart", timeout=5000)


def test_analytics_page_header(dashboard_page: Page):
    """Analytics page should display the correct header."""
    _go_to_analytics(dashboard_page)
    expect(dashboard_page.locator(".page-header h2")).to_have_text("Analytics")
    expect(dashboard_page.locator(".page-header p")).to_have_text("Visualize violation patterns and trends")


def test_analytics_charts_render(dashboard_page: Page):
    """All 4 analytics chart canvases should be present."""
    _go_to_analytics(dashboard_page)
    expect(dashboard_page.locator("#analyticsTrendChart")).to_be_visible()
    expect(dashboard_page.locator("#analyticsTypeChart")).to_be_visible()
    expect(dashboard_page.locator("#analyticsCameraChart")).to_be_visible()
    expect(dashboard_page.locator("#analyticsStatusChart")).to_be_visible()


def test_analytics_chart_cards_count(dashboard_page: Page):
    """There should be exactly 4 chart cards."""
    _go_to_analytics(dashboard_page)
    cards = dashboard_page.locator(".chart-card")
    expect(cards).to_have_count(4)


def test_analytics_chart_titles(dashboard_page: Page):
    """Each chart card should have a descriptive title."""
    _go_to_analytics(dashboard_page)
    titles = dashboard_page.locator(".chart-card h3")
    assert titles.count() == 4
    all_text = [titles.nth(i).text_content() for i in range(4)]
    assert any("Trend" in t for t in all_text)
    assert any("Type" in t for t in all_text)
    assert any("Camera" in t for t in all_text)
    assert any("Status" in t for t in all_text)


def test_analytics_filters_present(dashboard_page: Page):
    """Analytics filter controls should be visible."""
    _go_to_analytics(dashboard_page)
    expect(dashboard_page.locator("#analyticsDateFrom")).to_be_visible()
    expect(dashboard_page.locator("#analyticsDateTo")).to_be_visible()
    expect(dashboard_page.locator("#analyticsCameraFilter")).to_be_visible()
    expect(dashboard_page.locator("#analyticsViolationFilter")).to_be_visible()


def test_analytics_refresh_button(dashboard_page: Page):
    """Clicking refresh should re-render charts without errors."""
    _go_to_analytics(dashboard_page)
    refresh_btn = dashboard_page.locator("#btnRefreshAnalytics")
    expect(refresh_btn).to_be_visible()
    refresh_btn.click()
    dashboard_page.wait_for_timeout(500)
    # Charts should still be visible after refresh
    expect(dashboard_page.locator("#analyticsTrendChart")).to_be_visible()
