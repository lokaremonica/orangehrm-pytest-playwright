import pytest
import os
from playwright.sync_api import sync_playwright

os.makedirs("screenshots", exist_ok=True)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser, request):
    context = browser.new_context(locale="en-US")
    page = context.new_page()
    yield page

    # Always capture screenshot at the end
    screenshot_path = f"screenshots/{request.node.name}.png"
    page.screenshot(path=screenshot_path, full_page=True)
    context.close()


# ---------------- FIXED HOOK ----------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshots into pytest-html report if available."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        screenshot_path = f"screenshots/{item.name}.png"
        if os.path.exists(screenshot_path):
            extra = getattr(rep, "extra", [])
            from pytest_html import extras
            extra.append(extras.image(screenshot_path))
            rep.extra = extra
