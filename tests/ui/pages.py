from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

class LoginPage(BasePage):
    def navigate(self):
        self.page.goto("http://localhost:8080#login")
    
    def login(self, username, password):
        # Mock login flow since UI doesn't have a real login yet
        self.page.evaluate("() => { window.localStorage.setItem('auth', 'true'); }")
        self.page.goto("http://localhost:8080#dashboard")

class DashboardPage(BasePage):
    def wait_for_load(self):
        self.page.wait_for_selector(".page-header", state="attached")

class ReviewerQueuePage(BasePage):
    def navigate(self):
        self.page.goto("http://localhost:8080#cases")
        self.page.wait_for_selector("#caseTable", state="attached")

    def filter_by_status(self, status: str):
        self.page.select_option("#filterStatus", status)
        self.page.click("#btnApplyFilters")

    def get_row_count(self) -> int:
        return self.page.locator("#caseTableBody tr").count()

    def open_first_case(self):
        self.page.locator("#caseTableBody tr").first.click()

class CaseDetailPage(BasePage):
    def wait_for_load(self):
        self.page.wait_for_selector(".detail-grid", state="attached")
    def submit_decision(self, action: str, notes: str = ""):
        if notes:
            self.page.fill("#decisionNotes", notes)
        # Using data-attribute for robust selector strategy
        self.page.click(f"button[data-decision='{action}']")

class AdminAssignmentPage(BasePage):
    def navigate(self):
        # Mock admin assignment page (UI doesn't have this yet, stubbing for future)
        self.page.goto("http://localhost:8080#admin")

    def assign_case(self, case_id: str, reviewer_id: str):
        pass

class AnalyticsPage(BasePage):
    def navigate(self):
        self.page.goto("http://localhost:8080#analytics")
        self.page.wait_for_selector("#analyticsTrendChart", state="attached")
        
    def verify_charts_loaded(self):
        expect(self.page.locator("#analyticsTrendChart")).to_be_attached()
        expect(self.page.locator("#analyticsTypeChart")).to_be_attached()
