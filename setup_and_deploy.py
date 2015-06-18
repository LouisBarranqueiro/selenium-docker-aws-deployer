# -*- coding: utf-8 -*-
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
    # AWS URL
    AWS_URL = "http://aws.amazon.com"
    # AWS credentials
    AWS_LOGIN = ""
    AWS_PASSWORD = ""

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
        # # go on the `django-docker-starter` GitHub repository and fork repository
        # self.fork_github_repo()
        # # create automated build repository on DockerHub
        # self.create_dockerhub_build_repo()

    def login_into_github(self):
        """ Login into DockerHub
        """

        driver = self.driver
        driver.get(self.GITHUB_URL)
        driver.find_element_by_link_text("Sign in").click()
        driver.find_element_by_id("login_field").clear()
        driver.find_element_by_id("login_field").send_keys(self.GITHUB_LOGIN)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.GITHUB_PASSWORD)
        driver.find_element_by_name("commit").click()

    def fork_github_repo(self):
        """ Fork the `django-docker-starter`
        """

        driver = self.driver
        # login into GitHub
        self.login_into_github()
        driver.get(self.GITHUB_STARTER_REPO_URL)
        driver.find_element_by_xpath("//button[@type='submit']").click()

    def login_into_dockerhub(self):
        """ Login into DockerHub
        """
        driver = self.driver
        driver.get(self.DOCKER_HUB_URL + "/account/signup/")
        driver.find_element_by_link_text("Log In").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("developer.mail.no.reply@gmail.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("euc-dMB-y52-ZQT")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()

    def create_dockerhub_build_repo(self):
        """
            Create an automated build repository on DockerHub with the forked repository
            and wait build of container
        """

        driver = self.driver
        # login into DockerHub
        self.login_into_dockerhub()
        driver.find_element_by_link_text("+ Add Repository").click()
        driver.find_element_by_link_text("Automated Build").click()
        driver.find_element_by_link_text("Select").click()
        driver.find_element_by_link_text("developergithubnoreply").click()
        driver.find_element_by_css_selector("[href=\"https://registry.hub.docker.com/builds/github/" + self.GITHUB_LOGIN + "/" + self.GITHUB_STARTER_REPO_NAME + "/\"]").click()
        driver.find_element_by_name("action").click()
        # Wait during build of container (3min)
        time.sleep(3 * 60)

    def login_into_tutum(self):
        """ Login into Tutum
        """
        driver = self.driver
        driver.get(self.TUTUM_URL)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.TUTUM_LOGIN)
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.TUTUM_PASSWORD)
        driver.find_element_by_xpath("//button[@type='submit']").click()

    def login_into_aws(self):
        """ Login into AWS
        """

        driver = self.driver
        driver.get(self.AWS_URL)
        driver.find_element_by_link_text("AWS Management Console").click()
        driver.find_element_by_id("ap_email").clear()
        driver.find_element_by_id("ap_email").send_keys("developer.mail.no.reply@gmail.com")
        driver.find_element_by_id("ap_password").clear()
        driver.find_element_by_id("ap_password").send_keys("euc-dMB-y52-ZQT")
        driver.find_element_by_id("signInSubmit-input").click()

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
