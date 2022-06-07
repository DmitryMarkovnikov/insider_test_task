import time

from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class OpenPositionsPage(BasePage):

    _locator_open_positions_h3 = (By.XPATH, "//div[@class='col-12 text-center']//h3")
    _locator_open_positions_p = (By.XPATH, "//div[@class='col-12 text-center']//p")
    _locator_filter_by_location_dropdown = (By.ID, "select2-filter-by-location-container")
    _locator_filter_by_department_dropdown = (By.ID, "select2-filter-by-department-container")
    _locator_filter_by_department_value = (By.XPATH, "//span[@id='select2-filter-by-department-container']")
    _locator_filter_by_items = (By.XPATH, "//li[@class='select2-results__option']")
    _locator_jobs_list = (By.ID, "jobs-list")
    _locator_jobs_list_value = (By.XPATH, "//div[@id='jobs-list']/div//p")
    _locator_jobs_list_position_department = (By.XPATH, "//span[@class='position-department text-large font-weight-600 text-primary']") # noqa
    _locator_jobs_list_position_location = (By.XPATH, "//div[@class='position-location text-large']")
    _locator_position_apply_now_button = (By.XPATH, "//div[@class='position-list-item-wrapper bg-light']//a[contains(@class, 'btn-navy')]") # noqa

    _xpath_apply_to_chosen_position = "//p[text()='{position_title}']/..//a"

    def __init__(self, driver):
        super().__init__(driver)
        self._verify_page()

    def _verify_page(self):
        assert self.get_text(self._locator_open_positions_h3) != ""
        assert self.get_text(self._locator_open_positions_p) != ""
        self.get_element_present(self._locator_filter_by_location_dropdown, visible=True)
        self.get_element_present(self._locator_filter_by_department_dropdown, visible=True)

    def filter_by_location(self, location_name):
        """
        """
        self.select_from_drop_down_by_text(drop_down_locator=self._locator_filter_by_location_dropdown,
                                           option_locator=self._locator_filter_by_items,
                                           option_text=location_name)

    def filter_by_department(self, department_name):
        """
        """
        self.select_from_drop_down_by_text(drop_down_locator=self._locator_filter_by_department_dropdown,
                                           option_locator=self._locator_filter_by_items,
                                           option_text=department_name)

    def get_value_of_department_filter(self):
        return self.get_text(self._locator_filter_by_department_value)

    def get_position_titles(self):
        time.sleep(0.5)  # waiting for filters to be applied
        self.scroll_element_into_view(self._locator_jobs_list_value)
        elements = self.get_elements_present(self._locator_jobs_list_value, visible=True)
        return [self.get_text(element) for element in elements]

    def get_position_locations(self):
        time.sleep(1)  # waiting for filters to be applied
        self.scroll_element_into_view(self._locator_jobs_list_value)
        elements = self.get_elements_present(self._locator_jobs_list_position_location, visible=True)
        return [self.get_text(element) for element in elements]

    def get_position_departments(self):
        time.sleep(0.5)  # waiting for filters to be applied
        self.scroll_element_into_view(self._locator_jobs_list_value)
        elements = self.get_elements_present(self._locator_jobs_list_position_department, visible=True)
        return [self.get_text(element) for element in elements]

    def click_apply_to_of_position(self, exact_position_name):
        self.scroll_element_into_view(self._locator_jobs_list_value)
        locator = (By.XPATH, self._xpath_apply_to_chosen_position.format(position_title=exact_position_name))
        self.click(locator)

    def verify_apply_button_exists(self):
        element = self.get_element_present(self._locator_position_apply_now_button)
        return True if self.hover(element) else False

    def verify_jobs_list_exists(self):
        self.scroll_element_into_view(self._locator_jobs_list_value)
        self.get_element_present(self._locator_jobs_list_value, visible=True)
