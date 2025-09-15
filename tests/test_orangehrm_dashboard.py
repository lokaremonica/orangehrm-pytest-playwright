import pytest
from utils.config import BASE_URL, TEST_USERS, EXPECTED_GRIDS
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage


def test_orangehrm_role_based_dashboard(page):
    for case in TEST_USERS:
        login = LoginPage(page)
        dashboard = DashboardPage(page)
        admin = AdminPage(page)

        login.goto(BASE_URL)
        login.login(case["username"], case["password"])

        if case["expected"] == "admin":
            print("✅ Logged in as Admin")
            admin.go_to_admin()
            admin.add_ess_user("John Doe", "johndoe", "Password123")
            print("✅ ESS User created")
            dashboard.logout()

        elif case["expected"] == "ess":
            count = dashboard.verify_quick_launch_cards(EXPECTED_GRIDS["ess"])
            print(f"✅ ESS Quick Launch verified with {count} cards")
            dashboard.logout()

        else:
            pytest.fail(f"❌ Unexpected role {case['expected']}")