from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class BaseSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def fill_input_field(self, placeholder, content):
        xpath = "//input[@placeholder='{}']".format(placeholder)
        input_field = self.browser.find_element_by_xpath(xpath)
        input_field.send_keys(content)

    def login(self, username, password, *, use_navbar_link=False):
        if use_navbar_link:
            self.browser.find_element_by_link_text('Login').click()
        else:
            self.browser.get(self.live_server_url + '/accounts/login')
        self.fill_input_field('Username', username)
        self.fill_input_field('Password', password)
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
