import json
import pytest
from playwright.sync_api import Page, expect
from tests.ui.pages import LoginPage, ReviewerQueuePage, CaseDetailPage, AdminAssignmentPage, AnalyticsPage

def test_reviewer_queue_accept_case(mock_api: Page):
    """reviewer queue -> open case -> accept case"""
    queue_page = ReviewerQueuePage(mock_api)
    queue_page.navigate()
    
    # Open case
    queue_page.open_first_case()
    
    detail_page = CaseDetailPage(mock_api)
    detail_page.wait_for_load()
    
    # Accept case
    api_called = {"called": False}
    def intercept_review(route, request):
        api_called["called"] = True
        assert json.loads(request.post_data)["action"] == "APPROVE"
        route.fulfill(status=200, body='{"status": "success"}')
        
    mock_api.route("**/review", intercept_review)
    detail_page.accept_case(notes="Clear violation")
    
    assert api_called["called"]

def test_reviewer_queue_reject_case(mock_api: Page):
    """reviewer queue -> open case -> reject or escalate case"""
    queue_page = ReviewerQueuePage(mock_api)
    queue_page.navigate()
    queue_page.open_first_case()
    
    detail_page = CaseDetailPage(mock_api)
    detail_page.wait_for_load()
    
    api_called = {"called": False}
    def intercept_review(route, request):
        api_called["called"] = True
        assert json.loads(request.post_data)["action"] == "REJECT"
        route.fulfill(status=200, body='{"status": "success"}')
        
    mock_api.route("**/review", intercept_review)
    detail_page.reject_case(notes="False positive")
    assert api_called["called"]

def test_search_filter_verify_results(mock_api: Page):
    """search/filter -> verify filtered result list"""
    queue_page = ReviewerQueuePage(mock_api)
    queue_page.navigate()
    queue_page.filter_by_status("OPEN")
    
    # conftest returns MOCK_INCIDENTS_OPEN_ONLY which has 2 items
    assert queue_page.get_row_count() == 2

def test_admin_assignment_assign_case(mock_api: Page):
    """admin assignment -> assign case to reviewer"""
    # Note: Admin assignment UI is pending development, so we ensure the POM is ready.
    admin_page = AdminAssignmentPage(mock_api)
    admin_page.navigate()
    admin_page.assign_case("INC-001", "rev_01")
    # Assertions will be added when UI is built

def test_analytics_verify_charts(mock_api: Page):
    """analytics page -> verify chart section renders and key KPI widgets load"""
    analytics_page = AnalyticsPage(mock_api)
    analytics_page.navigate()
    analytics_page.verify_charts_loaded()
