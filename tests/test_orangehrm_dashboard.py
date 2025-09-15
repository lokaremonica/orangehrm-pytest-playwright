import pytest
from utils.config import BASE_URL, TEST_USERS, EXPECTED_GRIDS
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage


@pytest.mark.parametrize("case", TEST_USERS, ids=[u["username"] for u in TEST_USERS])
def test_orangehrm_role_based_dashboard(page, case):
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    admin = AdminPage(page)

    # Step 1: Login
    login.goto(BASE_URL)
    login.login(case["username"], case["password"])
    page.attach(f"{case['username']}_after_login")

    # ------------------ ADMIN FLOW ------------------
    if case["expected"] == "admin":
        admin.go_to_admin()
        page.attach(f"{case['username']}_admin_page")

        admin.add_ess_user("joker john selvam", "johndoe", "Password123")
        page.attach(f"{case['username']}_ess_user_created")

        dashboard.logout()
        page.attach(f"{case['username']}_after_logout")

    # ------------------ ESS FLOW ------------------
    elif case["expected"] == "ess":
        count = dashboard.verify_quick_launch_cards(EXPECTED_GRIDS["ess"])
        assert count == EXPECTED_GRIDS["ess"], f"Expected {EXPECTED_GRIDS['ess']} cards, found {count}"
        page.attach(f"{case['username']}_ess_dashboard")

        dashboard.logout()
        page.attach(f"{case['username']}_after_logout")

    # ------------------ INVALID FLOW ------------------
    # elif case["expected"] == "invalid":
    #     error = page.locator("p.oxd-alert-content-text")
    #     assert error.is_visible(), "Error message not shown for invalid login"
    #     assert "Invalid credentials" in error.inner_text()
    #     page.attach(f"{case['username']}_invalid_login")

    else:
        page.attach(f"{case['username']}_unexpected_role")
        pytest.fail(f"❌ Unexpected role {case['expected']}")
