from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class TeamsBasePage(BasePage):

    _locator_see_all_jobs_button = (By.XPATH, "//a[contains(text(), 'jobs')]")

    def __init__(self, driver):
        super().__init__(driver)
        self._verify_page()

    def _verify_page(self):
        self.get_element_present(self._locator_see_all_jobs_button)

    def open_all_jobs(self):
        self.click(self._locator_see_all_jobs_button)
