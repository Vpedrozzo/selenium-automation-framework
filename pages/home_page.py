from selenium.webdriver.common.by import By

class HomePage:
    URL = "https://the-internet.herokuapp.com/"

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    def click_form_authentication(self):
        self.driver.find_element(By.LINK_TEXT, "Form Authentication").click()
