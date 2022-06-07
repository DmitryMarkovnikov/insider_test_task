from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage
from settings import ui_settings


class HomePage(BasePage):

    _locator_header_navbar = (By.ID, "navbarNavDropdown")
    _locator_popup = (By.ID, "img-image-1650716561614")
    _locator_close_popup_button = (By.ID, "icon-close-button-1454703945249")
    _locator_more_drop_down = (By.XPATH, "//span[text()='More']/parent::a")
    _locator_more_drop_down_items = (By.XPATH, "//a[@class='d-flex flex-column flex-fill']//h5")

    def __init__(self, driver):
        super().__init__(driver, base_url=ui_settings.base_ui_url)
        self.open()
        self._verify_page()

    def _verify_page(self):
        self.get_element_present(self._locator_header_navbar, visible=True)
        self.close_popup_if_present()

    def close_popup_if_present(self):
        """
        Closes "Insider as a Leader in the IDC MarketScape" popup window if presents.
        """
        if self.is_element_present(self._locator_popup):
            self.click(self._locator_close_popup_button, timeout=5)

    def open_more_dropdown_and_go_to_page_by_item_text(self, dropdown_item_text):
        self.select_from_drop_down_by_text(drop_down_locator=self._locator_more_drop_down,
                                           option_locator=self._locator_more_drop_down_items,
                                           option_text=dropdown_item_text)
