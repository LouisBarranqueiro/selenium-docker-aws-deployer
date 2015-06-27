# -*- coding: utf-8 -*-
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
import unittest
import time
import logging

class AWSDeployer(object):
    def __init__(self):
        """ Init driver and read json config file
        """

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.config = None
        # read config file
        with open("config.json") as file:
            self.config = json.load(file)

    def launch_deployement(self):
        """ Login into Github account and fork the "django-docker-started" repository
        """

        # go on the `django-docker-starter` GitHub repository and fork repository
        self.fork_github_repo()
        # create automated build repository on DockerHub
        self.create_dockerhub_build_repo()
        # create `tutum` user on AWS
        tutum_access_key_id, tutum_secret_access_key = self.create_tutum_user_on_aws()
        # link AWS account to Tutum
        if tutum_access_key_id != None and tutum_secret_access_key != None:
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
        driver.get(self.config["gitHub"]["url"])
        if self.is_element_present_by_css_selector("a[href=\"/login\"]"):
            driver.find_element_by_css_selector("a[href=\"/login\"]").click()
            driver.find_element_by_id("login_field").clear()
            driver.find_element_by_id("login_field").send_keys(self.config["gitHub"]["credentials"]["name"])
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys(self.config["gitHub"]["credentials"]["password"])
            driver.find_element_by_name("commit").click()

    def fork_github_repo(self):
        """ Fork the `django-docker-starter`
        """

        driver = self.driver
        # login into GitHub
        self.login_into_github()
        # fork the `django-docker-starter` repository if it's not the case
        if not self.is_element_present_by_css_selector("#repo_listing .fork a[href=\"/" + self.config["gitHub"]["credentials"]["name"] + "/" + self.config["gitHub"]["starterRepository"][
            "name"] + "\"]"):
            driver.get(self.config["gitHub"]["url"] + self.config["gitHub"]["starterRepository"]["owner"] + "/" + self.config["gitHub"]["starterRepository"]["name"] + ".git")
            driver.find_element_by_xpath("//button[@type='submit']").click()

    def login_into_dockerhub(self):
        """ Login into Docker Hub
        """
        driver = self.driver
        driver.get(self.config["dockerHub"]["url"])
        if self.is_element_present_by_css_selector("a[href=\"/account/login/\"]"):
            driver.find_element_by_css_selector("a[href=\"/account/login/\"]").click()
            driver.find_element_by_id("id_username").clear()
            driver.find_element_by_id("id_username").send_keys(self.config["dockerHub"]["credentials"]["name"])
            driver.find_element_by_id("id_password").clear()
            driver.find_element_by_id("id_password").send_keys(self.config["dockerHub"]["credentials"]["password"])
            driver.find_element_by_css_selector("input.btn.btn-primary").click()

    def create_dockerhub_build_repo(self):
        """
        Create an automated build repository on DockerHub with the forked repository
        and wait build of container
        """

        driver = self.driver
        # login into DockerHub
        self.login_into_dockerhub()
        # create an automated build repository if it doesn't already exist
        if not self.is_element_present_by_css_selector("#rightcol .row a[href=\"/u/" + self.config["dockerHub"]["credentials"]["name"] + "/" + self.config["dockerHub"]["repository"][
            "name"] + "/\"]"):
            driver.get(self.config["dockerHub"]["url"] + "/builds/add/")
            driver.find_element_by_css_selector(".content .add-build .github a[href=\"/builds/github/select/\"]").click()
            driver.find_element_by_link_text(self.config["gitHub"]["credentials"]["name"]).click()
            driver.find_element_by_css_selector("[href=\"https://registry.hub.docker.com/builds/github/" +
                                                self.config["gitHub"]["credentials"]["name"] + "/" + self.config["gitHub"]["starterRepository"]["name"] + "/\"]").click()
            driver.find_element_by_id("id_repo_name").clear()
            driver.find_element_by_id("id_repo_name").send_keys(self.config["dockerHub"]["repository"]["name"])
            # change visibility of repository
            if self.config["dockerHub"]["repository"]["visibility"] == "private":
                driver.find_element_by_id("id_repo_visibility_1").click()

            driver.find_element_by_name("action").click()
            # wait during initialization of container
            driver.get(self.config["dockerHub"]["url"])

            # wait until docker image be built
            # while not self._is_visible("#rightcol .row a[href=\"/u/" + self.config["dockerHub"]["credentials"]["name"] + "/" + self.config["dockerHub"]["repository"]["name"] + "/\"] .stars-and-downloads-container"):
            #     driver.get(self.config["dockerHub"]["url"])

    def login_into_tutum(self):
        """ Login into Tutum
        """
        driver = self.driver
        driver.get(self.config["tutum"]["url"])

        driver.find_element_by_link_text("Login").click()
        if self.is_element_present("id", "id_username"):
            driver.find_element_by_id("id_username").clear()
            driver.find_element_by_id("id_username").send_keys(self.config["tutum"]["credentials"]["email"])
            driver.find_element_by_id("id_password").clear()
            driver.find_element_by_id("id_password").send_keys(self.config["tutum"]["credentials"]["password"])
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
        time.sleep(5)
        # create a node if it doesn't exist
        if not self.is_element_present_by_link_text(self.config["tutum"]["node"]["name"]):
            driver.find_element_by_css_selector("a[href=\"/node/launch/\"]").click()
            driver.find_element_by_id("node-cluster-name").clear()
            driver.find_element_by_id("node-cluster-name").send_keys(self.config["tutum"]["node"]["name"])
            # short delay to load javascript functions
            time.sleep(5)
            driver.find_element_by_id("btn-finish-node-cluster").click()

            # wait until docker image be built
            while not self._is_visible(".main-container-inner .status-container .status .green"):
                pass

    def create_tutum_service(self):
        """ Create a Tutum service based on the docker container previously built
        """

        driver = self.driver
        # login into Tutum
        self.login_into_tutum()
        driver.find_element_by_link_text("Services").click()
        driver.execute_script("$(\".cluster-link a\").text($(\".cluster-link a\").clone().children().remove().end().text())")
        # create a service if it doesn't exist
        if not self.is_element_present_by_link_text(self.config["tutum"]["service"]["name"]):
            driver.find_element_by_css_selector("a[href=\"/container/launch/\"]").click()
            driver.find_element_by_link_text("Public images").click()
            driver.find_element_by_link_text("Search Docker hub").click()
            driver.find_element_by_id("search").clear()
            driver.find_element_by_id("search").send_keys(self.config["dockerHub"]["repository"]["name"])
            # wait until docker image be available
            while not self._is_visible("#community-search-result button[data-image-name*=\"" + self.config["dockerHub"]["repository"]["name"] + "\"]"):
                driver.find_element_by_id("search").clear()
                driver.find_element_by_id("search").send_keys(self.config["dockerHub"]["repository"]["name"])

            driver.find_element_by_css_selector("button[data-image-name*=\"" + self.config["dockerHub"]["repository"]["name"] + "\"]").click()
            driver.find_element_by_id("app-name").clear()
            driver.find_element_by_id("app-name").send_keys(self.config["tutum"]["service"]["name"])
            # short delay to load javascript functions
            time.sleep(3)
            driver.find_element_by_css_selector("div.overlay.overlay-override").click()
            driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()
            driver.find_element_by_xpath("//div[@id='image-ports-wrapper']/div/div/div/table/tbody/tr/td[4]/span").click()
            driver.find_element_by_css_selector("input.form-control.input-sm").clear()
            driver.find_element_by_css_selector("input.form-control.input-sm").send_keys(self.config["tutum"]["service"]["port"])
            driver.find_element_by_id("step-container").click()
            driver.find_element_by_id("btn-deploy-services").click()
            # short delay to launch the service
            time.sleep(5)
            # wait until container is running
            while not self._is_visible("#cluster-status .green"):
                pass
        else:
            driver.find_element_by_link_text(self.config["tutum"]["service"]["name"]).click()

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
        driver.get(self.config["aws"]["url"])
        if self.is_element_present("id", "ap_email") and self.is_element_present("id", "ap_password"):
            driver.find_element_by_id("ap_email").clear()
            driver.find_element_by_id("ap_email").send_keys(self.config["aws"]["credentials"]["email"])
            driver.find_element_by_id("ap_password").clear()
            driver.find_element_by_id("ap_password").send_keys(self.config["aws"]["credentials"]["password"])
            driver.find_element_by_id("signInSubmit-input").click()

    def create_tutum_user_on_aws(self):
        """ Create a user (name: tutum) on AWS
        """

        driver = self.driver
        # login into AWS
        self.login_into_aws()
        driver.find_element_by_css_selector("a.service[data-service-id=\"iam\"]").click()
        driver.find_element_by_link_text("Users").click()
        # create a `tutum` user if he doesn't exist
        if not self.is_element_present_by_css_selector("table[data-table=\"resource\"] td[title=\"tutum\"]"):
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
        if not self.is_element_present("text", "tutum"):
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
        Check if an element exist by css selector
        :param css_selector: css selector
        :return: Boolean
        """

        try:
            self.driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException as e:
            return False
        return True

    def is_element_present_by_link_text(self, link_text):
        """
        Check if an element exist by link text
        :param link_text: link text
        :return: Boolean
        """

        try:
            self.driver.find_element_by_link_text(link_text)
        except NoSuchElementException as e:
            return False
        return True

    def _is_visible(self, locator, timeout = 2):
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
            return True
        except TimeoutException:
            return False
