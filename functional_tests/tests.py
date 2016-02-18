import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver

User = get_user_model()

from groups.models import Group, Player


class TeamsTest(StaticLiveServerTestCase):

    def setUp(self):
        nv = Group.objects.create(name='Nahlaot Volleyball')
        ts = Group.objects.create(name='Tel-Aviv Socker')

        Player.objects.create(name='Noam', score=4, group=nv)
        Player.objects.create(name='Ron', score=9, group=nv)
        Player.objects.create(name='Guy', score=3, group=nv)
        Player.objects.create(name='Yael', score=5, group=nv)
        Player.objects.create(name='Yaniv', score=2, group=ts)
        Player.objects.create(name='Arik', score=8, group=ts)
        Player.objects.create(name='Gonen', score=6, group=ts)
        Player.objects.create(name='Jacob', score=11, group=ts)

        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def change_player_state(self, player, button_text):
        xpath_template = "//a[contains(., '{}')]/span[contains(., '{}')]/p"
        xpath = xpath_template.format(player, button_text)
        self.browser.find_element_by_xpath(xpath).click()

    def parse_teams(self):
        """When on the 'teams' page, returns a set of sets of players."""
        # Sanity check, to make sure I'm on the right page
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('suggested teams', header.text)

        teams = set()
        dom_teams = self.browser.find_elements_by_css_selector('.list-group')
        for dom_team in dom_teams:
            players = dom_team.find_elements_by_tag_name('a')
            players.pop(0)  # Remove the team name from the list
            teams.add(frozenset(player.text for player in players))
        return teams

    def click_create_teams(self):
        xpath = "//button[contains(., 'Create teams!')]"
        self.browser.find_element_by_xpath(xpath).click()

    def set_num_of_teams(self, num_of_teams):
        inputbox = self.browser.find_element_by_id('id_number_of_teams')
        inputbox.clear()
        inputbox.send_keys(num_of_teams)

    def test_simple_two_teams_creation(self):
        # Moshe enter the site
        self.browser.get(self.live_server_url)

        # He sees the right title
        self.assertIn('Xteams!', self.browser.title)

        # He clicks the Nahlaot Volleyball group
        self.browser.find_element_by_link_text('Nahlaot Volleyball').click()

        # He move some players to the court and creates teams
        self.change_player_state('Noam', 'Move to court')
        self.change_player_state('Ron', 'Move to court')
        self.click_create_teams()

        # Now he sees the results
        teams = self.parse_teams()
        expected = {frozenset({'Ron'}), frozenset({'Noam'})}
        self.assertEqual(teams, expected)

    def test_not_enough_players_to_create_teams(self):
        # Now, Moshe wants to create 3 teams
        # but there are only 2 players on the court
        group = Group.objects.get(name='Nahlaot Volleyball')
        self.browser.get(self.live_server_url + group.get_absolute_url())

        self.change_player_state('Noam', 'Move to court')
        self.change_player_state('Ron', 'Move to court')

        self.set_num_of_teams(3)
        self.click_create_teams()

        error = self.browser.find_element_by_css_selector('.alert-danger')
        self.assertIn('not enough players', error.text.lower())

    def test_sane_team_up(self):
        # Moshe wants to create teams for real, and expect the teams to have
        # similar overal strength
        group = Group.objects.get(name='Tel-Aviv Socker')
        self.browser.get(self.live_server_url + group.get_absolute_url())

        self.change_player_state('Yaniv', 'Move to court')  # score: 2
        self.change_player_state('Arik', 'Move to court')  # score: 8
        self.change_player_state('Gonen', 'Move to court')  # score: 6
        self.change_player_state('Jacob', 'Move to court')  # score: 11

        self.click_create_teams()

        teams = self.parse_teams()
        expected = {frozenset({'Yaniv', 'Jacob'}),
                    frozenset({'Arik', 'Gonen'})}
        self.assertEqual(teams, expected)


class AccountManagementTest(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_user(username='Yossi', password='secret_password')
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.close()

    def fill_input_field(self, placeholder, content):
        xpath = "//input[@placeholder='{}']".format(placeholder)
        input_field = self.browser.find_element_by_xpath(xpath)
        input_field.send_keys(content)

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

    def test_register(self):
        self.assertUserLoggedOut()

        self.browser.find_element_by_link_text('Register').click()
        self.fill_input_field('Username', 'Moshe')
        self.fill_input_field('Password', 'secret_password')
        self.fill_input_field('Password confirmation', 'secret_password')
        self.submit()

        # Once registered users are redirected to home page again
        self.assertEqual(self.browser.current_url.strip('/'),
                         self.live_server_url.strip('/'))
        self.assertUserLoggedIn()

    def test_login_and_logout(self):
        self.assertUserLoggedOut()

        self.browser.find_element_by_link_text('Login').click()
        self.fill_input_field('Username', 'Yossi')
        self.fill_input_field('Password', 'secret_password')
        self.submit()

        self.assertEqual(self.browser.current_url.strip('/'),
                         self.live_server_url.strip('/'))
        self.assertUserLoggedIn()

        self.browser.find_element_by_link_text('Logout').click()
        self.assertUserLoggedOut()
