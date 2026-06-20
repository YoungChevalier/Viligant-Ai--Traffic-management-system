"""
test_cases.py
Tests for the #cases view: incident list, filters, pagination, sorting, quick actions.
"""
import pytest
from playwright.sync_api import Page, expect


def _go_to_cases(page: Page):
    page.click(".sidebar-nav a[href='#cases']")
    page.wait_for_selector("#caseTable", timeout=5000)


def test_case_list_renders_rows(dashboard_page: Page):
    """The case table should render the correct number of incident rows."""
    _go_to_cases(dashboard_page)
    rows = dashboard_page.locator("#caseTableBody tr")
    expect(rows).to_have_count(5)


def test_case_list_displays_incident_id(dashboard_page: Page):
    """Each row should display the incident ID."""
    _go_to_cases(dashboard_page)
    first_row = dashboard_page.locator("#caseTableBody tr").first
    expect(first_row).to_contain_text("INC-2026-")


def test_case_list_has_status_badges(dashboard_page: Page):
    """Status badges should render with appropriate text."""
    _go_to_cases(dashboard_page)
    badges = dashboard_page.locator("#caseTableBody .badge")
    assert badges.count() >= 5


def test_case_list_has_view_buttons(dashboard_page: Page):
    """Each OPEN case should have View, Quick Approve, Quick Reject buttons."""
    _go_to_cases(dashboard_page)
    view_buttons = dashboard_page.locator("button[data-action='view']")
    assert view_buttons.count() >= 1


def test_filter_by_status_open(dashboard_page: Page):
    """Filtering by OPEN status should show only open cases."""
    _go_to_cases(dashboard_page)
    dashboard_page.select_option("#filterStatus", "OPEN")
    dashboard_page.click("#btnApplyFilters")
    dashboard_page.wait_for_timeout(500)
    rows = dashboard_page.locator("#caseTableBody tr")
    # Mock intercept returns MOCK_INCIDENTS_OPEN_ONLY (2 rows)
    expect(rows).to_have_count(2)


def test_clear_filters_restores_all(dashboard_page: Page):
    """Clearing filters should restore the full case list."""
    _go_to_cases(dashboard_page)
    dashboard_page.select_option("#filterStatus", "OPEN")
    dashboard_page.click("#btnApplyFilters")
    dashboard_page.wait_for_timeout(300)
    dashboard_page.click("#btnClearFilters")
    dashboard_page.wait_for_timeout(500)
    rows = dashboard_page.locator("#caseTableBody tr")
    expect(rows).to_have_count(5)


def test_pagination_info_displays(dashboard_page: Page):
    """Pagination info text should show the correct range."""
    _go_to_cases(dashboard_page)
    pagination = dashboard_page.locator("#pagination .page-info")
    expect(pagination).to_contain_text("Showing")
    expect(pagination).to_contain_text("of 5 cases")


def test_sort_header_click_toggles_arrow(dashboard_page: Page):
    """Clicking a sortable column header should toggle the sort arrow."""
    _go_to_cases(dashboard_page)
    date_header = dashboard_page.locator("th[data-sort='timestamp']")
    date_header.click()
    dashboard_page.wait_for_timeout(300)
    arrow = date_header.locator(".sort-arrow")
    expect(arrow).to_have_class_containing("active")


def test_click_row_navigates_to_detail(dashboard_page: Page):
    """Clicking a case row (not on a button) should navigate to case detail."""
    _go_to_cases(dashboard_page)
    first_row = dashboard_page.locator("#caseTableBody tr").first
    first_row.click()
    dashboard_page.wait_for_timeout(500)
    expect(dashboard_page).to_have_url_containing("#case/INC-2026-")


def test_quick_approve_shows_toast(dashboard_page: Page):
    """Clicking the quick approve button should show a success toast."""
    _go_to_cases(dashboard_page)
    approve_btn = dashboard_page.locator("button[data-action='quick-approve']").first
    approve_btn.click()
    dashboard_page.wait_for_timeout(500)
    toast = dashboard_page.locator(".toast-success")
    expect(toast).to_be_visible()


def test_filters_bar_has_all_controls(dashboard_page: Page):
    """The filters bar should contain status, violation, camera, plate, and date inputs."""
    _go_to_cases(dashboard_page)
    expect(dashboard_page.locator("#filterStatus")).to_be_visible()
    expect(dashboard_page.locator("#filterViolation")).to_be_visible()
    expect(dashboard_page.locator("#filterCamera")).to_be_visible()
    expect(dashboard_page.locator("#filterPlate")).to_be_visible()
    expect(dashboard_page.locator("#filterDateFrom")).to_be_visible()
    expect(dashboard_page.locator("#filterDateTo")).to_be_visible()
