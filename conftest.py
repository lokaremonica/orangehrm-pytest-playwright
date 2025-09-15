import os
import pytest
from playwright.sync_api import sync_playwright
from pytest_html import extras


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

    # Keep track of screenshots taken during this test
    request.node._screenshot_paths = []

    def save_and_attach(name: str):
        """Helper to take screenshot and record path"""
        os.makedirs("screenshots", exist_ok=True)
        path = os.path.join("screenshots", f"{name}.png")
        page.screenshot(path=path, full_page=True)
        request.node._screenshot_paths.append(path)
        return path

    # Expose helper to the test
    page.attach = save_and_attach

    yield page
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach all screenshots (success + failure) to pytest-html report"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and hasattr(item, "_screenshot_paths"):
        rep.extras = getattr(rep, "extras", [])

        for path in item._screenshot_paths:
            if os.path.exists(path):
                rep.extras.append(extras.image(path))
