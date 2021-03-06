import unittest

from django.contrib.auth import get_user_model

from .base import BaseSeleniumTestCase
from groups.models import Group, Player

User = get_user_model()


class TeamsTest(BaseSeleniumTestCase):

    def setUp(self):
        super().setUp()
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
        self.submit()

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
        self.submit()

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
        self.submit()

        teams = self.parse_teams()
        expected = {frozenset({'Yaniv', 'Jacob'}),
                    frozenset({'Arik', 'Gonen'})}
        self.assertEqual(teams, expected)


class AccountManagementTest(BaseSeleniumTestCase):

    def setUp(self):
        super().setUp()
        User.objects.create_user(username='Yossi', password='secret_password')
        self.browser.get(self.live_server_url)

    def test_register(self):
        self.assertUserLoggedOut()

        self.browser.find_element_by_link_text('Register').click()
        self.fill_input_field('Username', 'Moshe')
        self.fill_input_field('Password', 'secret_password')
        self.fill_input_field('Password confirmation', 'secret_password')
        self.submit()

        # Once registered users are redirected to home page again
        self.assertInHomePage()
        self.assertUserLoggedIn()

    def test_login_and_logout(self):
        self.assertUserLoggedOut()
        self.login('Yossi', 'secret_password', use_navbar_link=True)

        self.assertInHomePage()
        self.assertUserLoggedIn()

        self.browser.find_element_by_link_text('Logout').click()
        self.assertUserLoggedOut()


class GroupManagementTest(BaseSeleniumTestCase):

    def setUp(self):
        super().setUp()
        User.objects.create_user(username='Moshe', password='secret_password')
        self.login('Moshe', 'secret_password')
        self.group = 'Basketball with Moshe'

    def test_create_group(self):
        self.browser.get(self.live_server_url)
        self.create_group(self.group, use_homepage_button=True)

        # Moshe was redirected to the group page
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn(self.group, header.text)

        # Moshe goes back to the homepage to make he manage the group
        self.browser.find_element_by_link_text('Xteams!').click()
        group_element = self.find_group_element(self.group)
        self.assertIn('Managed', group_element.text)

    def test_manage_group_add_players(self):
        self.create_group(self.group)
        self.browser.find_element_by_link_text('Manage').click()

        self.fill_input_field('Name', 'Moshe')
        self.fill_input_field('Score', 1000)
        self.submit()

        # There is a player for Moshe
        players = self.browser.find_element_by_id('players')
        self.assertIn('Moshe', players.text)

    def test_change_group_name(self):
        self.create_group(self.group)
        self.browser.find_element_by_link_text('Manage').click()

        new_group_name = 'Volleyball with Nevet'
        self.fill_input_field('Group name', new_group_name, clear=True)
        self.submit()

        # Check the new name is in the title and the old one is gone
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn(new_group_name, header.text)
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.group, body_text)

    def test_delete_group(self):
        self.create_group(self.group)
        self.browser.find_element_by_link_text('Manage').click()

        self.browser.find_element_by_link_text('Delete group').click()
        self.submit()

        # Check the group name doesn't appear in the homepage
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(self.group, body_text)
