import pytest
from pages.home_page import HomePage

def test_navigate_to_login(driver):
    home = HomePage(driver)
    home.load()
    home.click_form_authentication()
    assert "login" in driver.current_url
