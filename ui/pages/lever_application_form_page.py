from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class LeverApplicationFormPage(BasePage):
    _locator_posting_headline = (By.CLASS_NAME, "posting-headline")
    _locator_position_title = (By.XPATH, "//div[@class='posting-headline']/h2")

    _xpath_position_title = "//h2[text()='{position_title}']"

    def __init__(self, driver):
        super().__init__(driver)
        self._verify_page()

    def _verify_page(self):
        self.get_element_present(self._locator_posting_headline, visible=True)

    def get_position_title(self):
        return self.get_text(self._locator_position_title)
