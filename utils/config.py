BASE_URL = "https://opensource-demo.orangehrmlive.com/"

TEST_USERS = [
    {"username": "Admin", "password": "admin123", "expected": "admin"},
    {"username": "johndoe", "password": "Password123", "expected": "ess"}
    # {"username": "fakeuser", "password": "wrongpass", "expected": "invalid"},
]

EXPECTED_GRIDS = {
    "admin": 6,
    "ess": 3,
}
