from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time


class SeleniumGithub(unittest.TestCase):
    # GitHub URL
    GITHUB_URL = "https://github.com/"
    # GitHub credentials
    GITHUB_LOGIN = "developergithubnoreply"
    GITHUB_PASSWORD = "eRm-dpW-qkd-34f-!"
    # GitHub `django-docker-starter` repository info
    GITHUB_STARTER_REPO_NAME = "django-docker-starter"
    GITHUB_STARTER_REPO_URL = "https://github.com/lbsb/" + GITHUB_STARTER_REPO_NAME + ".git"
    # Docker Hub URL
    DOCKER_HUB_URL = "https://hub.docker.com"
    # Docker Hub credentials
    DOCKER_HUB_LOGIN = "developer.mail.no.reply@gmail.com"
    DOCKER_HUB_PASSWORD = "euc-dMB-y52-ZQT"
    # Tutum URL
    TUTUM_URL = "https://www.tutum.co"
    # Tutum credentials
    TUTUM_LOGIN = "developer.mail.no.reply@gmail.com"
    TUTUM_PASSWORD = "euc-dMB-y52-ZQT"

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
        # login into GitHub
        driver.get(self.GITHUB_URL)
        driver.find_element_by_link_text("Sign in").click()
        driver.find_element_by_id("login_field").clear()
        driver.find_element_by_id("login_field").send_keys(self.GITHUB_LOGIN)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.GITHUB_PASSWORD)
        driver.find_element_by_name("commit").click()
        # go on the `django-docker-starter` GitHub repository
        driver.get(self.GITHUB_STARTER_REPO_URL)
        # fork repository
        driver.find_element_by_xpath("//button[@type='submit']").click()
        # Login into Docker Hub
        driver.get(self.DOCKER_HUB_URL + "/account/signup/")
        driver.find_element_by_link_text("Log In").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("developer.mail.no.reply@gmail.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("euc-dMB-y52-ZQT")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        # create automated build repository
        driver.find_element_by_link_text("+ Add Repository").click()
        driver.find_element_by_link_text("Automated Build").click()
        driver.find_element_by_link_text("Select").click()
        driver.find_element_by_link_text("developergithubnoreply").click()
        driver.find_element_by_css_selector("[href=\"https://registry.hub.docker.com/builds/github/" + self.GITHUB_LOGIN + "/" + self.GITHUB_STARTER_REPO_NAME + "/\"]").click()
        driver.find_element_by_name("action").click()
        # Wait during build of container (3min)
        time.sleep(3 * 60)
        # Login into Tutum
        driver.get(self.TUTUM_URL)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.TUTUM_LOGIN)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.TUTUM_PASSWORD)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        # create a new service
        driver.find_element_by_link_text("Services").click()
        driver.find_element_by_link_text("Create your first service").click()
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys(self.GITHUB_STARTER_REPO_NAME)
        driver.find_element_by_xpath("//button[@onclick='selectImage(this)']").click()
        driver.find_element_by_id("show-more").click()
        driver.find_element_by_xpath("//button[2]").click()
        driver.find_element_by_id("btn-create-services").click()

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
