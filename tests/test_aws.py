import unittest

import seleniumpy

from pages import IAMHomePage


class WebTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = seleniumpy.webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()


class TestSetupIAMRole(WebTestCase):

    def test_iam_setup(self):
        iam_home_page = IAMHomePage(self.driver).open()
        iam_roles_page = iam_home_page.click_roles()
        create_new_role_page = iam_roles_page.create_new_role()
        create_new_role_page.select_aws_lambda()
        create_new_role_page.filter("AWSLambdaBasicExecutionRole")
        create_new_role_page.check("AWSLambdaBasicExecutionRole")
        create_new_role_page.filter("AWSLambdaVPCAccessExecutionRole")
        create_new_role_page.check("AWSLambdaVPCAccessExecutionRole")
        create_new_role_page.next_step()
        create_new_role_page.role_name = "mbed_time_series_database2"
        create_new_role_page.create_role()
