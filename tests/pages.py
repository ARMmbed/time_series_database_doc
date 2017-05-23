import os
from time import sleep
from netrc import netrc
from cookielib import Cookie

import seleniumpy
from interruptingcow import timeout
from cookiestxt import MozillaCookieJar
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException


class Page(object):

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.go(self.URL)
        return self.wait_until_loaded()

    def wait_until_loaded(self):
        raise NotImplementedError()


class LoginPage(Page):

    def login(self, email=None, password=None):
        if email is None or password is None:
            email, password = self.get_credentials()
        self.driver.wait_for(name="email").text = email
        self.driver.find(name="password").text = password
        self.driver.find(id="signInSubmit-input").click()
        ## TODO: figure out a better place to put these
        #self.save_cookies('awscookies.txt')

    def get_credentials(self):
        try:
            email = os.environ['AWS_EMAIL']
            password = os.environ['AWS_PASSWORD']
        except KeyError:
            email, _, password = netrc().authenticators("amazon.com")
        return email, password

    def save_cookies(self, filename):
        cj = MozillaCookieJar()
        cookies = self.driver.get_cookies()
        for c in cookies:
            version = 1
            name = c['name']
            value = c['value']
            port = c.get('port', None)
            port_specified = port is not None
            domain = c['domain']
            domain_specified = True
            domain_initial_dot = domain.startswith('.')
            path = c['path']
            path_specified = True
            secure = c['secure']
            expires = c.get('expiry', None)
            discard = False
            comment = None
            comment_url = None
            rest = {}
            cookie = Cookie(version, name, value, port, port_specified, domain, domain_specified, domain_initial_dot, path, path_specified, secure, expires, discard, comment, comment_url, rest)
            cj.set_cookie(cookie)
        cj.save(filename, ignore_discard=True, ignore_expires=True)


class AWSAuthPage(Page):

    URL = None

    def open(self):
        #self.load_cookies('awscookies.txt')
        self.driver.go(self.URL)
        if 'Sign In or Create' in self.driver.page_source:
            login_page = LoginPage(self.driver)
            login_page.login()
        return self.wait_until_loaded()

    def load_cookies(self, filename):
        cj = MozillaCookieJar()
        cj.load(filename, ignore_discard=True, ignore_expires=True)
        for cookie in cj:
            dct = {
                'name': cookie.name,
                'value': cookie.value,
            }
            try:
                self.driver.add_cookie(dct)
            except WebDriverException, e:
                if "current domain" in e.msg.lower():
                    pass
                else:
                    raise


class IAMHomePage(AWSAuthPage):

    URL = "https://console.aws.amazon.com/iam/home?region=us-east-1#/home"

    def wait_until_loaded(self):
        self.driver.wait_for(id="iam-container")
        return self

    def click_roles(self):
        self.driver.find(class_name="roles").find(tag_name='a').click()
        return IAMRolesPage(self.driver).wait_until_loaded()


class IAMRolesPage(AWSAuthPage):

    URL = "https://console.aws.amazon.com/iam/home?region=us-east-1#/roles"

    def wait_until_loaded(self):
        self.driver.wait_for(class_name="create_role")
        return self

    def create_new_role(self):
        self.driver.find(class_name="create_role").click()
        return IAMCreateNewRolePage(self.driver).wait_until_loaded()


class IAMCreateNewRolePage(AWSAuthPage):

    def wait_until_loaded(self):
        self.driver.wait_for(class_name="wizard-content")
        self.driver.wait_for(class_name="policy_table")
        return self

    def select_aws_lambda(self):
        table = self.driver.find(class_name="policy_table")
        rows = table.find_all(tag_name="tr")
        for row in rows:
            if "AWS Lambda" in row.text:
                row.find(tag_name="button").click()
                break

    def filter(self, text):
        # TODO: figure out how to make this reliable without using timeout
        trying = True
        with timeout(5):
            while trying:
                try:
                    input = self.driver.wait_for(class_name="search_input")
                    input.text = text
                except StaleElementReferenceException:
                    pass
                else:
                    trying = False

    def check(self, text):
        # TODO: figure out how to make this reliable without using timeout
        trying = True
        with timeout(5):
            while trying:
                table = [t for t in self.driver.find_all(tag_name="table") \
                         if t['data-table'] == 'resource'][0]
                rows = table.find(tag_name="tbody").find_all(tag_name="tr")
                for row in rows:
                    try:
                        cols = row.find_all(tag_name="td")
                    except StaleElementReferenceException:
                        break
                    else:
                        if cols[2]['title'] == text:
                            row.find(class_name="control_checkbox").click()
                            trying = False
                            break

    def next_step(self):
        self.driver.find(class_name="next").click()

    @property
    def role_name(self):
        return self.driver.find(id="role_name").text

    @role_name.setter
    def role_name(self, text):
        self.driver.find(id="role_name").text = text

    def create_role(self):
        button = self.driver.find(class_name="next")
        assert button.text == "Create role"
        button.click()
