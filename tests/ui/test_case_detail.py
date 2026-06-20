"""
test_case_detail.py
Tests for the #case/:id view: evidence image, metadata, review history,
and the critical decision workflow (approve/reject/escalate).
"""
import json
import pytest
from playwright.sync_api import Page, expect


def _go_to_case_detail(page: Page, incident_id: str = "INC-2026-00001"):
    page.goto(f"http://localhost:8080#case/{incident_id}")
    page.wait_for_selector(".detail-grid", timeout=5000)


def test_case_detail_renders_header(dashboard_page: Page):
    """The case detail page should show the incident ID in the header."""
    _go_to_case_detail(dashboard_page)
    header = dashboard_page.locator(".page-header h2")
    expect(header).to_contain_text("INC-2026-00001")


def test_case_detail_status_badge(dashboard_page: Page):
    """The current status badge should be visible."""
    _go_to_case_detail(dashboard_page)
    badge = dashboard_page.locator(".page-header .badge")
    expect(badge).to_be_visible()


def test_evidence_image_present(dashboard_page: Page):
    """The evidence image should be rendered."""
    _go_to_case_detail(dashboard_page)
    img = dashboard_page.locator("#evidenceImg")
    expect(img).to_be_visible()
    src = img.get_attribute("src")
    assert src is not None and len(src) > 0


def test_metadata_fields_rendered(dashboard_page: Page):
    """Key metadata fields should be visible."""
    _go_to_case_detail(dashboard_page)
    expect(dashboard_page.locator("text=Violation Type")).to_be_visible()
    expect(dashboard_page.locator("text=Detection Confidence")).to_be_visible()
    expect(dashboard_page.locator("text=License Plate")).to_be_visible()
    expect(dashboard_page.locator("text=Camera ID")).to_be_visible()


def test_violation_type_displays_correctly(dashboard_page: Page):
    """The violation type should match the mock data."""
    _go_to_case_detail(dashboard_page)
    # Find the meta-value next to "Violation Type" label
    meta_rows = dashboard_page.locator(".meta-row")
    first_value = meta_rows.first.locator(".meta-value")
    expect(first_value).to_have_text("NO_HELMET")


def test_confidence_bar_renders(dashboard_page: Page):
    """Confidence bars should render with percentage labels."""
    _go_to_case_detail(dashboard_page)
    bars = dashboard_page.locator(".confidence-bar")
    assert bars.count() >= 1
    # Check that a bar label contains a percentage
    bar_label = bars.first.locator(".bar-label")
    text = bar_label.text_content()
    assert "%" in text


def test_back_button_returns_to_cases(dashboard_page: Page):
    """Clicking '← Back to Cases' should navigate back to #cases."""
    _go_to_case_detail(dashboard_page)
    dashboard_page.click("#btnBackToList")
    dashboard_page.wait_for_timeout(500)
    expect(dashboard_page).to_have_url_containing("#cases")


def test_decision_form_present(dashboard_page: Page):
    """The decision form with textarea and 3 action buttons should be present."""
    _go_to_case_detail(dashboard_page)
    expect(dashboard_page.locator("#decisionNotes")).to_be_visible()
    expect(dashboard_page.locator("button[data-decision='APPROVE']")).to_be_visible()
    expect(dashboard_page.locator("button[data-decision='REJECT']")).to_be_visible()
    expect(dashboard_page.locator("button[data-decision='ESCALATE']")).to_be_visible()


def test_reject_workflow_sends_api_and_shows_toast(dashboard_page: Page):
    """
    CRITICAL FLOW: Clicking Reject should:
    1. Submit a POST to /incidents/:id/review
    2. Show a success toast
    """
    _go_to_case_detail(dashboard_page)

    # Fill in notes
    dashboard_page.fill("#decisionNotes", "This is a false positive.")

    # Track the API call
    api_called = {"called": False, "payload": None}

    def intercept_review(route, request):
        api_called["called"] = True
        api_called["payload"] = json.loads(request.post_data or "{}")
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "status": "success",
                "data": {"incident_id": "INC-2026-00001", "action": "REJECT", "new_status": "REJECTED"}
            })
        )

    dashboard_page.route("**/review", intercept_review)

    # Click Reject
    dashboard_page.click("button[data-decision='REJECT']")
    dashboard_page.wait_for_timeout(1000)

    # Verify API was called with correct payload
    assert api_called["called"], "The review API should have been called."
    assert api_called["payload"]["action"] == "REJECT"

    # Verify toast appeared
    toast = dashboard_page.locator(".toast")
    expect(toast).to_be_visible()


def test_approve_workflow(dashboard_page: Page):
    """
    CRITICAL FLOW: Clicking Approve should submit the decision.
    """
    _go_to_case_detail(dashboard_page)
    dashboard_page.click("button[data-decision='APPROVE']")
    dashboard_page.wait_for_timeout(1000)
    toast = dashboard_page.locator(".toast")
    expect(toast).to_be_visible()


def test_escalate_workflow(dashboard_page: Page):
    """
    CRITICAL FLOW: Clicking Escalate should submit the escalation.
    """
    _go_to_case_detail(dashboard_page)
    dashboard_page.fill("#decisionNotes", "Unclear image, needs admin review.")
    dashboard_page.click("button[data-decision='ESCALATE']")
    dashboard_page.wait_for_timeout(1000)
    toast = dashboard_page.locator(".toast")
    expect(toast).to_be_visible()


def test_review_history_section_present(dashboard_page: Page):
    """The review history section should be present."""
    _go_to_case_detail(dashboard_page)
    history = dashboard_page.locator(".review-history")
    expect(history).to_be_visible()
    expect(dashboard_page.locator("text=Review History")).to_be_visible()
