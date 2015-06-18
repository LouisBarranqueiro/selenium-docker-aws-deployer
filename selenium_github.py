from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest


class SeleniumGithub(unittest.TestCase):
    GITHUB_URL = "https://github.com/"
    # GitHub credentials
    GITHUB_LOGIN = "developergithubnoreply"
    GITHUB_PASSWORD = "eRm-dpW-qkd-34f-!"
    # GitHub `django-docker-starter` repository info
    GITHUB_STARTER_REPO_NAME = "django-docker-starter"
    GITHUB_STARTER_REPO_URL = "https://github.com/lbsb/" + GITHUB_STARTER_REPO_NAME + ".git"

    def setUp(self):
        """ Setup
        """
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.BASE_URL = self.GITHUB_URL
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_fork_repository(self):
        """ Login into Github account and fork the "django-docker-started" repository
        """

        driver = self.driver
        driver.get(self.BASE_URL)
        driver.find_element_by_link_text("Sign in").click()
        # login into GitHub
        driver.find_element_by_id("login_field").clear()
        driver.find_element_by_id("login_field").send_keys(self.GITHUB_LOGIN)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.GITHUB_PASSWORD)
        driver.find_element_by_name("commit").click()
        # go on the `django-docker-starter` GitHub repository
        driver.get(self.GITHUB_STARTER_REPO_URL)
        # fork repository
        driver.find_element_by_xpath("//button[@type='submit']").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by = how, value = what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
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
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
