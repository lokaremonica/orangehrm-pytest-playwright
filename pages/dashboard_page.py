from playwright.sync_api import expect


class DashboardPage:
    def __init__(self, page):
        self.page = page

    def verify_quick_launch_cards(self, expected_count):
        quick_launch_grid = self.page.locator("div.orangehrm-quick-launch")
        expect(quick_launch_grid).to_be_visible(timeout=10000)
        cards = quick_launch_grid.locator("div.orangehrm-quick-launch-card")
        count = cards.count()
        assert count == expected_count, f"❌ Expected {expected_count} Quick Launch cards, found {count}"
        return count

    def logout(self):
        self.page.click("p.oxd-userdropdown-name")
        self.page.click("a:has-text('Logout')")
