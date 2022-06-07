import abc
import time
from typing import Union
from typing import Tuple

from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    _locator_accept_all_cookies_button = (By.ID, "wt-cli-accept-all-btn")

    def __init__(self, driver, base_url=None, explicit_wait=10):

        self.driver = driver
        self._explicit_wait = explicit_wait
        self.base_url = base_url

    @abc.abstractmethod
    def _verify_page(self):
        pass

    def open(self):
        """
        Opens base url
        """
        self.driver.get(self.base_url)

    def get_title(self):
        """
        Gets title of a page
        """
        return self.driver.title

    def get_url(self):
        """
        Gets current url of a page
        """
        return self.driver.current_url

    def click(self, locator, params=None, timeout=None):
        """
        Clicks web element.
        :param locator: locator tuple or WebElement instance
        :param params: locator parameters
        :param timeout: time to wait for element, _explicit_wait by default.
        """
        element = locator
        if not isinstance(element, WebElement):
            element = self._get(locator, EC.element_to_be_clickable, params, timeout, "Element is not clickable!")
        element.click()

    def _get(self, locator: Union[Tuple[str, str], WebElement], expected_condition,
             params=None, timeout=None, message="", **kwargs):
        """
        Gets element(s) based on locator with optional parameters.
        Uses selenium.webdriver.support.expected_conditions to determine the state of the element(s).
        :param locator: locator tuple or WebElement instance
        :param expected_condition: expected condition of element (ie. visible, clickable, etc)
        :param params: locator parameters
        :param timeout: time to wait for element, _explicit_wait by default
        :message
        :param kwargs: optional arguments to expected conditions
        :return: WebElement instance, list of WebElements, or None
        """

        exp_cond = expected_condition(locator, **kwargs)
        if timeout == 0:
            try:
                return exp_cond(self.driver)
            except NoSuchElementException:
                return None

        if timeout is None:
            timeout = self._explicit_wait

        error_msg = "Expected condition: {} \nTimeout: {}".format(expected_condition, timeout)
        message += error_msg

        return WebDriverWait(self.driver, timeout).until(exp_cond, error_msg)

    def select_from_drop_down_by_value(self, locator, value, params=None):
        """
        Select option from drop down widget using value.
        :param locator: locator tuple or WebElement instance
        :param value: string
        :param params: (optional) locator parameters
        :return: None
        """
        from selenium.webdriver.support.ui import Select

        element = locator
        if not isinstance(element, WebElement):
            element = self.get_element_present(locator, params)

        Select(element).select_by_value(value)

    def get_text(self, locator, params=None, timeout=None, visible=True):
        """
        Get text or value from element based on locator with optional parameters.
        :param locator: locator tuple or WebElement
        :param params: locator parameters
        :param timeout: time to wait for text
        :param visible: should element be visible before getting text
        :return: element text, value or empty string
        """
        element = locator
        if not isinstance(element, WebElement):
            element = self.get_element_present(locator, params, timeout, visible)

        if element and element.text:
            return element.text
        else:
            try:
                return element.get_attribute('value')
            except AttributeError:
                return ""

    def select_from_drop_down_by_text(self, drop_down_locator, option_locator, option_text, params=None):
        """
        Selects option from drop down.
        :param drop_down_locator: locator tuple or WebElement instance
        :param option_locator: locator tuple
        :param option_text: text to base option selection on
        :param params: dictionary of params
        :return: None
        """
        # Open/activate drop down
        self.click(drop_down_locator, params['drop_down'] if params else None)

        # Get options
        for option in self.get_elements_present(option_locator, params['option'] if params else None):
            if self.get_text(option) == option_text:
                self.click(option)
                break

    def get_element_present(self, locator, params=None, timeout=None, visible=False):
        """
        Gets element present in the DOM.
        :param locator: element identifier
        :param params: (optional) locator parameters
        :param timeout: (optional) time to wait for element (default: self._explicit_wait)
        :param visible: (optional) if the element should also be visible (default: False)
        :return: WebElement instance
        """
        error_msg = "Element is not present!"
        expected_condition = EC.visibility_of_element_located if visible else EC.presence_of_element_located
        return self._get(locator, expected_condition, params, timeout, error_msg)

    def get_elements_present(self, locator, params=None, timeout=None, visible=False):
        """
        Get elements present in the DOM.
        :param locator: locator
        :param params: locator parameters
        :param timeout: time to wait for element
        :param visible: flag if the element should be visible
        :return: WebElement instance
        """
        error_msg = "Elements are not present!"
        expected_condition = EC.visibility_of_all_elements_located if visible else EC.presence_of_all_elements_located
        return self._get(locator, expected_condition, params, timeout, error_msg)

    def is_element_present(self, locator, visible=True):
        """
        Returns True if element is present, else False
        :param locator: locator tuple
        :param visible: flag if the element should be visible
        :return: True or False
        """
        try:
            self.get_element_present(locator, visible=visible)
            return True
        except TimeoutException as e:
            return False

    def scroll_element_into_view(self, selector):
        """
        Scrolls an element into view.
        :param selector: selector of element or WebElement to scroll into view
        :return: None
        """
        element = selector
        if isinstance(element, WebElement):
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        else:
            self.driver.execute_script("arguments[0].scrollIntoView();", self.get_element_present(element))

    def scroll_to_the_top(self):
        """
        Scrolls to very top of the page
        :return: None
        """
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_using_action_chain(self,  element, mark="+"):
        """
        Scrolls to the element using Action Chains
        :param element: WebElement
        :param mark: plus or minus scroll down if + and scroll up if -
        :return: None
        """
        searching = True
        action_chains = ActionChains(self.driver)
        while searching:
            try:
                action_chains.move_to_element(element).perform()
                time.sleep(0.5)
                searching = False
            except MoveTargetOutOfBoundsException:
                self.driver.execute_script("window.scrollTo(0, window.scrollY {mark} 300)".format(mark=mark))
                time.sleep(0.5)

    def accept_all_cookies(self):
        """
        Clicks button to accept all cookies.
        :return: None
        """
        self.click(self._locator_accept_all_cookies_button)

    def hover(self, locator):
        """
        Hovers to an element.
        :param locator: locator tuple or WebElement instance
        :return: hovered element
        """
        element = locator
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        actions.reset_actions()
        return element
