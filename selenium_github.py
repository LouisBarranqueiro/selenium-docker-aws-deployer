import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class SeleniumGithub(unittest.TestCase):

    def setUp(self):
        """ Setup
        """
        self.GITHUB_URL = "https://github.com/"
        # GitHub credentials
        self.GITHUB_LOGIN = "developergithubnoreply"
        self.GITHUB_PASSWORD = "eRm-dpW-qkd-34f-!"
        # GitHub repository informations
        self.GITHUB_REPO_NAME = "selenium5"
        self.GITHUB_REPO_DESC = "Automated web test with selenium"
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.BASE_URL = self.GITHUB_URL
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_selenium_github(self):
        """ Login into Github account and create a new public repository
            and test if the repository is created
        """
        driver = self.driver
        driver.get(self.BASE_URL)
        driver.find_element_by_link_text("Sign in").click()
        # Login
        driver.find_element_by_id("login_field").clear()
        driver.find_element_by_id("login_field").send_keys(self.GITHUB_LOGIN)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.GITHUB_PASSWORD)
        driver.find_element_by_name("commit").click()
        # Create new repository
        driver.find_element_by_xpath("//ul[@id='user-links']/li[2]/a/span").click()
        driver.find_element_by_link_text("New repository").click()
        driver.find_element_by_id("repository_name").clear()
        driver.find_element_by_id("repository_name").send_keys(self.GITHUB_REPO_NAME)
        driver.find_element_by_id("repository_public_true").click()
        driver.find_element_by_id("repository_description").clear()
        driver.find_element_by_id("repository_description").send_keys(self.GITHUB_REPO_DESC)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        # Check existence of the repository previously created
        self.assertEqual(requests.head(self.BASE_URL + "/" + self.GITHUB_LOGIN + "/" + self.GITHUB_REPO_NAME).status_code, 200)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
