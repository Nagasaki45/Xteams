from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class BaseSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def find_group_element(self, group_name):
        """Return group element from the homepage groups list"""
        xpath = "//a[contains(., '{}')]".format(group_name)
        return self.browser.find_element_by_xpath(xpath)

    def fill_input_field(self, placeholder, content, clear=False):
        xpath = "//input[@placeholder='{}']".format(placeholder)
        input_field = self.browser.find_element_by_xpath(xpath)
        if clear:
            input_field.clear()
        input_field.send_keys(content)

    def login(self, username, password, *, use_navbar_link=False):
        if use_navbar_link:
            self.browser.find_element_by_link_text('Login').click()
        else:
            self.browser.get(self.live_server_url + '/accounts/login')
        self.fill_input_field('Username', username)
        self.fill_input_field('Password', password)
        self.submit()

    def create_group(self, group_name, *, use_homepage_button=False):
        if use_homepage_button:
            self.browser.find_element_by_link_text('Add a new group').click()
        else:
            self.browser.get(self.live_server_url + '/create')
        self.fill_input_field('Name', self.group)
        self.submit()

    def submit(self):
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

    def assertUserLoggedOut(self):
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Login', body_text)
        self.assertNotIn('Logout', body_text)

    def assertUserLoggedIn(self):
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Logout', body_text)
        self.assertNotIn('Login', body_text)

    def assertInHomePage(self):
        self.assertEqual(self.browser.current_url.strip('/'),
                         self.live_server_url.strip('/'))
