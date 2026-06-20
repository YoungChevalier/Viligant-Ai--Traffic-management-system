"""
conftest.py
Playwright fixtures and mock API route intercepts for dashboard UI tests.

All tests use `page.route()` to intercept XHR/fetch requests and return
pre-canned mock_responses, so NO live backend is needed.
"""

import json
import pytest
from playwright.sync_api import Page, Route, Request
from tests.ui.mock_responses import (
    MOCK_INCIDENTS_LIST,
    MOCK_STATS,
    MOCK_INCIDENT_DETAIL,
    MOCK_REVIEW_RESPONSE,
    MOCK_INCIDENTS_OPEN_ONLY
)

# The URL where the frontend SPA is served during testing.
# Start the frontend server with: uvicorn services.frontend.app.main:app --port 8080
FRONTEND_URL = "http://localhost:8080"


@pytest.fixture(scope="session")
def browser_context_args():
    """Default browser context: desktop viewport, no GPU."""
    return {
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }


def _handle_api_route(route: Route, request: Request):
    """
    Central handler that intercepts all API calls and returns mock JSON.
    This ensures tests are fully isolated from backend availability.
    """
    url = request.url

    # GET /incidents/stats
    if "/incidents/stats" in url:
        route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_STATS))
        return

    # GET /incidents/<id> (detail)
    if "/incidents/INC-" in url and "?" not in url and "/review" not in url:
        # Extract incident ID from the URL
        route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_INCIDENT_DETAIL))
        return

    # POST /incidents/<id>/review
    if "/review" in url and request.method == "POST":
        route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_REVIEW_RESPONSE))
        return

    # GET /incidents?status=OPEN...
    if "/incidents" in url and "status=OPEN" in url:
        route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_INCIDENTS_OPEN_ONLY))
        return

    # GET /incidents (default list)
    if "/incidents" in url:
        route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_INCIDENTS_LIST))
        return

    # GET /analytics/summary
    if "/analytics/summary" in url:
        route.fulfill(status=200, content_type="application/json", body=json.dumps(MOCK_STATS))
        return

    # Fallback: let it pass through (e.g., CDN scripts)
    route.continue_()


@pytest.fixture
def mock_api(page: Page):
    """
    Fixture that intercepts all API calls to localhost:8000 and localhost:8001
    and returns mock data. Applied automatically to each test.
    """
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGEERROR: {err}"))

    page.route("**/api/v1/**", _handle_api_route)
    yield page


@pytest.fixture
def dashboard_page(mock_api: Page):
    """Navigates to the frontend SPA and waits for the initial render."""
    mock_api.goto(FRONTEND_URL)
    # Wait for the SPA to finish its initial render (loading text disappears)
    mock_api.wait_for_selector(".page-header", timeout=5000)
    return mock_api
