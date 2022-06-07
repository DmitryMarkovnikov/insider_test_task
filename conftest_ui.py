import uuid

import allure
import pytest

from settings import ui_settings


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.executable_path = '/usr/local/bin/chromedriver'
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.binary = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
    firefox_options.add_argument('-foreground')
    firefox_options.set_preference('browser.anchor_color', '#FF0000')
    return firefox_options


@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot(ui_settings.screenshot_path + str(uuid.uuid4()) + '.png')

            # Attach screenshot to Allure report:
            allure.attach(browser.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)

            # For happy debugging:
            # logging.info('URL: ', browser.current_url)
            # logging.info('Browser logs:')
            # for log in browser.get_log('browser'):
            #     logging.info(log)
        except: # noqa
            pass  # just ignore any errors here



