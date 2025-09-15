from playwright.sync_api import expect


class AdminPage:
    def __init__(self, page):
        self.page = page

    def go_to_admin(self):
        self.page.click("a.oxd-main-menu-item:has(span:has-text('Admin'))")
        expect(self.page.locator("h5:has-text('System Users')")).to_be_visible(timeout=10000)

    def add_ess_user(self, employee_name, username, password):
        self.page.click("button:has-text('Add')")
        expect(self.page.locator("h6:has-text('Add User')")).to_be_visible(timeout=10000)

        # Role = ESS
        self.page.locator("div.oxd-select-text").nth(0).click()
        self.page.locator("div[role='listbox'] div:has-text('ESS')").click()

        # Status = Enabled
        self.page.locator("div.oxd-select-text").nth(1).click()
        self.page.locator("div[role='listbox'] div:has-text('Enabled')").click()

        # Employee Name
        self.page.fill("input[placeholder='Type for hints...']", employee_name)
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")

        # Username
        self.page.locator("div.oxd-input-group:has(label:has-text('Username')) input").fill(username)

        # Password
        form = self.page.locator("form.oxd-form")
        password_inputs = form.locator("input[type='password']")
        password_inputs.nth(0).fill(password)
        password_inputs.nth(1).fill(password)

        self.page.click("button:has-text('Save')")
        expect(self.page.locator("div.orangehrm-paper-container")).to_be_visible(timeout=10000)
