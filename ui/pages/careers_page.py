from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class CareersPage(BasePage):

    _locator_location_slider = (By.ID, "location-slider")
    _locator_teams = (By.ID, "career-find-our-calling")
    _locator_life_at_insider_header = (By.XPATH, "//h2[@class='elementor-heading-title elementor-size-default' and text()='Life at Insider']") # noqa
    _locator_life_at_insider_text = (By.XPATH, "//div[@data-id='fe38935']//p")
    _locator_life_at_insider_carousel = (By.XPATH, "//div[@data-id='c06d1ec']")
    _locator_scroll_to_see_teams_button = (By.XPATH, "//a[text()='See all teams']")

    _xpath_team_name_link = "//h3[contains(text(), '{team_name}')]/../../.."

    def __init__(self, driver):
        super().__init__(driver)
        self._verify_page()

    def _verify_page(self):
        # check location block presents
        self.scroll_element_into_view(self._locator_location_slider)
        self.get_element_present(self._locator_location_slider, visible=True)

        # check teams block presents
        self.scroll_element_into_view(self._locator_teams)
        self.get_element_present(self._locator_teams, visible=True)

        # check life at insider block presents and it's text is not blank
        self.scroll_element_into_view(self._locator_life_at_insider_header)
        self.get_element_present(self._locator_life_at_insider_carousel, visible=True)
        assert self.get_text(self._locator_life_at_insider_text) != ""
        self.scroll_to_the_top()

    def open_all_teams(self):
        el = self.get_element_present(self._locator_scroll_to_see_teams_button)
        self.scroll_using_action_chain(el)
        self.click(self._locator_scroll_to_see_teams_button)

    def choose_team(self, team_name):
        locator_team_link = (By.XPATH, self._xpath_team_name_link.format(team_name=team_name))
        el = self.get_element_present(locator_team_link)
        self.scroll_using_action_chain(el)

        self.click(locator_team_link)
