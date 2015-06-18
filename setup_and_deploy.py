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
    AWS_LOGIN = "developer.mail.no.reply@gmail.com"
    AWS_PASSWORD = "euc-dMB-y52-ZQT"

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
        # create `tutum` user on AWS
        tutum_access_kei_id, tutum_secret_access_key = self.create_tutum_user_on_aws()
        # link AWS account to Tutum
        self.link_aws_account_to_tutum(tutum_access_kei_id, tutum_secret_access_key)
        # create tutum service on Tutum
        # self.create_tutum_service()

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
        driver.find_element_by_css_selector("[data-dropdown=\"aws-nav-dropdown-account\"]").click()
        driver.find_element_by_css_selector("[data-dropdown=\"aws-nav-dropdown-account\"]").click()
        driver.find_element_by_link_text("AWS Management Console").click()
        driver.find_element_by_id("ap_email").clear()
        driver.find_element_by_id("ap_email").send_keys(self.AWS_LOGIN)
        driver.find_element_by_id("ap_password").clear()
        driver.find_element_by_id("ap_password").send_keys(self.AWS_PASSWORD)
        driver.find_element_by_id("signInSubmit-input").click()

    def create_tutum_user_on_aws(self):
        """ Create a user (name: tutum) on AWS
        """

        driver = self.driver
        # login into AWS
        self.login_into_aws()
        driver.find_element_by_xpath("//div[@id='serviceColumn2']/div/div/a[2]/div[2]").click()
        driver.find_element_by_link_text("Users").click()
        driver.find_element_by_xpath("//div[@id='c']/div[2]/div[2]/div/div/div/button").click()
        driver.find_element_by_css_selector("li > input").clear()
        driver.find_element_by_css_selector("li > input").send_keys("tutum")
        driver.find_element_by_xpath("//div[@id='c']/div/div[2]/div/div[2]/div[3]/div/button").click()
        driver.find_element_by_link_text("Show User Security Credentials").click()
        # Get information of `tutum` user
        tutum_access_key_id = driver.find_elements_by_class_name("attrValue")[0].text
        tutum_secret_access_key = driver.find_elements_by_class_name("attrValue")[1].text
        # Set policy for `tutum` user
        driver.find_element_by_css_selector("a.pointer.btn_close > strong").click()
        driver.find_element_by_css_selector("#closeWindow > strong").click()
        driver.find_element_by_css_selector("div.tableField").click()
        if driver.find_element_by_id("attachUserPolicy").is_displayed():
            driver.find_element_by_id("attachUserPolicy").click()
        else:
            driver.find_element_by_css_selector("div[data-target=\"#inlinePolicies\"]").click()
            driver.find_element_by_css_selector("a.pointer.attachInlinePolicy").click()

        driver.find_element_by_xpath("(//input[@name='accordion-radio'])[2]").click()
        driver.find_element_by_xpath("//div[@id='c']/div/div[2]/div/div/ol/li[2]/div[2]/div/div[2]/button").click()
        driver.find_element_by_id("policy_name").clear()
        driver.find_element_by_id("policy_name").send_keys("tutum-policy")
        driver.find_element_by_css_selector("button.btn.validatebtn").click()
        driver.find_element_by_xpath("//div[@id='c']/div/div[2]/div/div[2]/div[3]/div/button[2]").click()

        return tutum_access_key_id, tutum_secret_access_key

    def create_tutum_service(self):
        """ Create a tutum service based on the docker container previously builded
        """

        driver = self.driver
        service_available = False
        # login into tutum
        self.login_into_tutum()
        driver.find_element_by_link_text("Services").click()
        # first service
        if driver.find_element_by_link_text("Create your first service") > 0:
            driver.find_element_by_link_text("Create your first service").click()
            service_available = True
        # not the first service
        elif driver.find_element_by_link_text("Create service").size() > 0:
            driver.find_element_by_link_text("Create service").click()
            service_available = True

        if service_available:
            driver.find_element_by_link_text("Public images").click()
            driver.find_element_by_link_text("Search Docker hub").click()
            driver.find_element_by_id("search").clear()
            driver.find_element_by_id("search").send_keys("django-docker-starter")
            driver.find_element_by_id("search").clear()
            driver.find_element_by_id("search").send_keys(self.GITHUB_STARTER_REPO_NAME)
            driver.find_element_by_xpath("//button[@onclick='selectImage(this)']").click()
            driver.find_element_by_css_selector("div.overlay-message").click()
            driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()
            driver.find_element_by_xpath("//div[@id='image-ports-wrapper']/div/div/div/table/tbody/tr/td[4]/span").click()
            driver.find_element_by_css_selector("input.form-control.input-sm").clear()
            driver.find_element_by_css_selector("input.form-control.input-sm").send_keys("80")
            driver.find_element_by_id("step-container").click()
            driver.find_element_by_id("btn-deploy-services").click()

    def link_aws_account_to_tutum(self, tutum_access_key_id, tutum_secret_access_key):
        """ Link AWS account to Tutum
        """

        driver = self.driver
        # login into tutum
        self.login_into_tutum()
        driver.find_element_by_css_selector("span.user-info").click()
        driver.find_element_by_xpath("//div[@id='navbar-container']/div[2]/ul/li[3]/ul/li/a/i").click()
        driver.find_element_by_css_selector("div.aws-not-linked > #aws-link").click()
        driver.find_element_by_id("access-key").clear()
        driver.find_element_by_id("access-key").send_keys(tutum_access_key_id)
        driver.find_element_by_id("secret-access-key").clear()
        driver.find_element_by_id("secret-access-key").send_keys(tutum_secret_access_key)
        driver.find_element_by_id("aws-save-credentials").click()

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
