from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from teams.models import Team, Player


class SiteVisitorTest(LiveServerTestCase):

    def setUp(self):
        nv = Team.objects.create(name='Nahlaot Volleyball')
        ts = Team.objects.create(name='Tel-Aviv Socker')

        Player.objects.create(name='Noam', score=4, team=nv)
        Player.objects.create(name='Ron', score=9, team=nv)
        Player.objects.create(name='Guy', score=3, team=nv)
        Player.objects.create(name='Yael', score=5, team=nv)
        Player.objects.create(name='Yaniv', score=2, team=ts)
        Player.objects.create(name='Arik', score=8, team=ts)
        Player.objects.create(name='Gonen', score=6, team=ts)
        Player.objects.create(name='Jacob', score=9, team=ts)

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)  # set session timeout for queries

    def tearDown(self):
        self.browser.close()

    def click_player_checkbox(self, player):
        checkbox = self.browser.find_element_by_id('id_' + player)
        checkbox.click()

    def test_user_story(self):
        # Moshe enter the site
        self.browser.get(self.live_server_url)

        # He sees the right title
        self.assertIn('Xteams!', self.browser.title)

        # He looks at the list of available teams
        teams = self.browser.find_element_by_id('teams')

        # He clicks the Nahlaot Volleyball team
        team = self.browser.find_element_by_link_text('Nahlaot Volleyball')
        team.click()

        # He looks at the list of available players
        players = self.browser.find_element_by_id('players')

        # He select the inputbox to enter how many groups he wants
        inputbox = self.browser.find_element_by_id('id_num_of_groups')

        # And enter 3 (as for 3 groups)
        inputbox.send_keys('3')

        # He checks some players:
        self.click_player_checkbox('Noam')
        self.click_player_checkbox('Ron')
        self.click_player_checkbox('Guy')
        self.click_player_checkbox('Yael')

        # And click on submit.
        submit = self.browser.find_element_by_tag_name('button')
        submit.click()

        # Moshe now see the results
        self.fail('finish functional test')
