"""
test_dashboard.py
Tests for the #dashboard view: KPI cards rendering, chart canvases present.
"""
import pytest
from playwright.sync_api import Page, expect


def test_kpi_cards_render(dashboard_page: Page):
    """All 5 KPI cards should render with correct data from mock stats."""
    cards = dashboard_page.locator(".kpi-card")
    expect(cards).to_have_count(5)

    # Total Cases
    total_card = dashboard_page.locator(".kpi-total .kpi-value")
    expect(total_card).to_have_text("5")

    # Pending Review (OPEN)
    open_card = dashboard_page.locator(".kpi-open .kpi-value")
    expect(open_card).to_have_text("2")

    # Approved
    approved_card = dashboard_page.locator(".kpi-approved .kpi-value")
    expect(approved_card).to_have_text("1")

    # Rejected
    rejected_card = dashboard_page.locator(".kpi-rejected .kpi-value")
    expect(rejected_card).to_have_text("1")

    # Escalated
    escalated_card = dashboard_page.locator(".kpi-escalated .kpi-value")
    expect(escalated_card).to_have_text("1")


def test_kpi_labels_correct(dashboard_page: Page):
    """KPI labels should have meaningful text."""
    expect(dashboard_page.locator(".kpi-total .kpi-label")).to_have_text("Total Cases")
    expect(dashboard_page.locator(".kpi-open .kpi-label")).to_have_text("Pending Review")
    expect(dashboard_page.locator(".kpi-approved .kpi-label")).to_have_text("Approved")
    expect(dashboard_page.locator(".kpi-rejected .kpi-label")).to_have_text("Rejected")
    expect(dashboard_page.locator(".kpi-escalated .kpi-label")).to_have_text("Escalated")


def test_chart_canvases_present(dashboard_page: Page):
    """The 3 dashboard chart canvases should be present in the DOM."""
    expect(dashboard_page.locator("#dashTrendChart")).to_be_visible()
    expect(dashboard_page.locator("#dashTypeChart")).to_be_visible()
    expect(dashboard_page.locator("#dashCameraChart")).to_be_visible()


def test_charts_grid_layout(dashboard_page: Page):
    """Charts should be inside a .charts-grid container."""
    charts_grid = dashboard_page.locator(".charts-grid")
    expect(charts_grid).to_be_visible()
    chart_cards = charts_grid.locator(".chart-card")
    expect(chart_cards).to_have_count(3)


def test_page_header_dashboard(dashboard_page: Page):
    """The dashboard page header should display correctly."""
    expect(dashboard_page.locator(".page-header h2")).to_have_text("Dashboard")
    expect(dashboard_page.locator(".page-header p")).to_have_text("Real-time overview of traffic violation cases")
