# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time


class DjangoDockerAWS(unittest.TestCase):
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
    # Tutum node
    TUTUM_NODE_NAME = "django-node"
    # Tutum service
    TUTUM_SERVICE_NAME = "django-starter-app"
    # AWS URL
    AWS_URL = "http://console.aws.amazon.com"
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

    def test_deploy_django_docker_app_on_aws(self):
        """ Login into Github account and fork the "django-docker-started" repository
        """

        # go on the `django-docker-starter` GitHub repository and fork repository
        self.fork_github_repo()
        # create automated build repository on DockerHub
        self.create_dockerhub_build_repo()
        # create `tutum` user on AWS
        tutum_access_key_id, tutum_secret_access_key = self.create_tutum_user_on_aws()
        # link AWS account to Tutum
        self.link_aws_account_to_tutum(tutum_access_key_id, tutum_secret_access_key)
        # create tutum node on Tutum
        self.create_tutum_node()
        # create tutum service on Tutum
        app_ip = self.create_tutum_service()
        # Watch application
        self.watch_app(app_ip)

    def login_into_github(self):
        """ Login into DockerHub
        """

        driver = self.driver
        driver.get(self.GITHUB_URL)
        if self.is_element_present_by_css_selector("a[href=\"/login\"]"):
            driver.find_element_by_css_selector("a[href=\"/login\"]").click()
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
        driver.find_element_by_css_selector("a.repo-filter[data-filter=\".fork\"]").click()
        # fork the `django-docker-starter` repository if it's not the case
        if not self.is_element_present_by_css_selector(".repo-and-owner[title=*\"" + self.GITHUB_STARTER_REPO_NAME + "\""):
            driver.get(self.GITHUB_STARTER_REPO_URL)
            driver.find_element_by_xpath("//button[@type='submit']").click()

    def login_into_dockerhub(self):
        """ Login into Docker Hub
        """
        driver = self.driver
        driver.get(self.DOCKER_HUB_URL)
        if self.is_element_present_by_css_selector("a[href=\"/account/login/\"]"):
            driver.find_element_by_css_selector("a[href=\"/account/login/\"]").click()
            driver.find_element_by_id("id_username").clear()
            driver.find_element_by_id("id_username").send_keys(self.DOCKER_HUB_LOGIN)
            driver.find_element_by_id("id_password").clear()
            driver.find_element_by_id("id_password").send_keys(self.DOCKER_HUB_PASSWORD)
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
        driver.find_element_by_css_selector("[href=\"https://registry.hub.docker.com/builds/github/" +
                                            self.GITHUB_LOGIN + "/" + self.GITHUB_STARTER_REPO_NAME + "/\"]").click()
        driver.find_element_by_name("action").click()
        # Wait during build of container
        time.sleep(3.2 * 60)

    def login_into_tutum(self):
        """ Login into Tutum
        """
        driver = self.driver
        driver.get(self.TUTUM_URL)

        driver.find_element_by_link_text("Login").click()
        if self.is_element_present("id", "id_username"):
            driver.find_element_by_id("id_username").clear()
            driver.find_element_by_id("id_username").send_keys(self.TUTUM_LOGIN)
            driver.find_element_by_id("id_password").clear()
            driver.find_element_by_id("id_password").send_keys(self.TUTUM_PASSWORD)
            driver.find_element_by_xpath("//button[@type='submit']").click()

    def link_aws_account_to_tutum(self, tutum_access_key_id, tutum_secret_access_key):
        """
        Link AWS account to Tutum
        :param tutum_access_key_id: access key id of AWS tutum user
        :param tutum_secret_access_key: secret access key of AWS tutum user
        """

        driver = self.driver
        # login into tutum
        self.login_into_tutum()
        driver.find_element_by_css_selector("span.user-info").click()
        driver.find_element_by_xpath("//div[@id='navbar-container']/div[2]/ul/li[3]/ul/li/a/i").click()
        # link AWS account if there is no one
        if self.is_element_present_by_css_selector("div.aws-not-linked > #aws-link"):
            driver.find_element_by_css_selector("div.aws-not-linked > #aws-link").click()
            driver.find_element_by_id("access-key").clear()
            driver.find_element_by_id("access-key").send_keys(tutum_access_key_id)
            driver.find_element_by_id("secret-access-key").clear()
            driver.find_element_by_id("secret-access-key").send_keys(tutum_secret_access_key)
            driver.find_element_by_id("aws-save-credentials").click()
            time.sleep(5)

    def create_tutum_node(self):
        """ Create a Tutum node based on AWS
        """

        driver = self.driver
        # login into tutum
        self.login_into_tutum()
        driver.find_element_by_css_selector("a[href=\"/node/cluster/list/\"]").click()
        driver.find_element_by_css_selector("a[href=\"/node/launch/\"]").click()
        driver.find_element_by_id("node-cluster-name").clear()
        driver.find_element_by_id("node-cluster-name").send_keys(self.TUTUM_NODE_NAME)
        # short delay to load javascript functions
        time.sleep(5)
        driver.find_element_by_id("btn-finish-node-cluster").click()
        # wait for deployement of node
        time.sleep(2.5 * 60)

    def create_tutum_service(self):
        """ Create a Tutum service based on the docker container previously built
        """

        driver = self.driver
        # login into Tutum
        self.login_into_tutum()
        driver.find_element_by_link_text("Services").click()
        driver.find_element_by_css_selector("a[href=\"/container/launch/\"]").click()
        driver.find_element_by_link_text("Public images").click()
        driver.find_element_by_link_text("Search Docker hub").click()
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys("django-docker-starter")
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys(self.GITHUB_STARTER_REPO_NAME)
        driver.find_element_by_css_selector("button[data-image-name*=\"" + self.GITHUB_STARTER_REPO_NAME + "\"]").click()
        driver.find_element_by_id("app-name").clear()
        driver.find_element_by_id("app-name").send_keys(self.TUTUM_SERVICE_NAME)
        # short delay to load javascript functions
        time.sleep(3)
        driver.find_element_by_css_selector("div.overlay.overlay-override").click()
        driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()
        driver.find_element_by_xpath("//div[@id='image-ports-wrapper']/div/div/div/table/tbody/tr/td[4]/span").click()
        driver.find_element_by_css_selector("input.form-control.input-sm").clear()
        driver.find_element_by_css_selector("input.form-control.input-sm").send_keys("80")
        driver.find_element_by_id("step-container").click()
        driver.find_element_by_id("btn-deploy-services").click()
        # short delay to launch the service
        time.sleep(2 * 60)
        driver.find_element_by_css_selector("td.container-link.sortable.renderable > a").click()
        driver.find_element_by_css_selector("#node > a").click()
        driver.execute_script("document.getElementsByClassName('info-bar')[0].getElementsByClassName('icon-link')[0].remove()")
        node_ip = driver.find_element_by_xpath("//div[@class='info-bar']/div[@class='app-info'][1]").text

        return node_ip.replace("\"", "").replace(" ", "")

    def watch_app(self, ip):
        """
        Go on node ip to watch application in live
        :param ip: ip of an application
        :return:
        """

        driver = self.driver
        driver.get("http://" + ip)
        time.sleep(20)

    def login_into_aws(self):
        """ Login into AWS
        """

        driver = self.driver
        driver.get(self.AWS_URL)
        if self.is_element_present("id", "ap_email") and self.is_element_present("id", "ap_password"):
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
        driver.find_element_by_xpath("a.service[data-service-id=\"iam\"]").click()
        driver.find_element_by_link_text("Users").click()
        # create a `tutum` user if he doesn't exist
        if self.is_element_present_by_css_selector("td[title=\"tutum\"]"):
            driver.find_element_by_css_selector("button.create_user").click()
            driver.find_element_by_css_selector("li > input").clear()
            driver.find_element_by_css_selector("li > input").send_keys("tutum")
            driver.find_element_by_xpath("//div[@id='c']/div/div[2]/div/div[2]/div[3]/div/button").click()
            driver.find_element_by_link_text("Show User Security Credentials").click()
            # Get information of `tutum` user
            tutum_access_key_id = driver.find_elements_by_class_name("attrValue")[0].text
            tutum_secret_access_key = driver.find_elements_by_class_name("attrValue")[1].text
        else:
            tutum_access_key_id = None
            tutum_secret_access_key = None

        driver.find_element_by_link_text("Policies").click()
        if self.is_element_present_by_css_selector("button.getStarted"):
            driver.find_element_by_css_selector("button.getStarted").click()

        driver.find_element_by_css_selector("td[title=\"AmazonEC2FullAccess\"]").click()
        # Attach policy (full access to EC2) to `tutum` user if its not
        if self.is_element_present("text", "tutum"):
            driver.find_element_by_css_selector("button.attach").click()
            # short delay to load javascript functions
            time.sleep(5)
            driver.find_element_by_css_selector("div.tableField").click()
            driver.find_element_by_css_selector("button.submit").click()

        return tutum_access_key_id, tutum_secret_access_key

    def is_element_present(self, how, what):
        """
        Check if an element exist
        :param how: how to select it
        :param what: what to select
        :return: Boolean
        """

        try:
            self.driver.find_element(by = how, value = what)
        except NoSuchElementException as e:
            return False
        return True

    def is_element_present_by_css_selector(self, css_selector):
        """
        Check if an element exist
        :param css_selector: css selector
        :return: Boolean
        """

        try:
            self.driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException as e:
            return False
        return True

if __name__ == "__main__":
    unittest.main()
