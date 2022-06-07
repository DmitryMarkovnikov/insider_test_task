import logging

from assertpy import assert_that, soft_assertions

from ui.pages.careers_page import CareersPage
from ui.pages.home_page import HomePage
from ui.pages.lever_application_form_page import LeverApplicationFormPage
from ui.pages.open_positions_page import OpenPositionsPage
from ui.pages.teams_base_page import TeamsBasePage


class TestInsiderFlow:

    def test_insider_selenium_task(self, web_browser):

        home_page = HomePage(web_browser)
        home_page.accept_all_cookies()
        home_page.open_more_dropdown_and_go_to_page_by_item_text("Careers")
        careers_page = CareersPage(web_browser)
        careers_page.open_all_teams()
        careers_page.choose_team("Quality")
        team_page = TeamsBasePage(web_browser)  # basic TeamsBasePage is enough for that case
        team_page.open_all_jobs()
        qa_open_positions_page = OpenPositionsPage(web_browser)

        # assert qa department is chosen
        chosen_department = qa_open_positions_page.get_value_of_department_filter()
        if "\n" in chosen_department:
            chosen_department = chosen_department[2:]
        with soft_assertions():
            assert_that(chosen_department).is_equal_to_ignoring_case("quality assurance")

        # check that job list is not empty
        qa_open_positions_page.verify_jobs_list_exists()

        # choose location
        qa_open_positions_page.filter_by_location(location_name="Istanbul, Turkey")
        qa_open_positions_page.filter_by_department(department_name="Quality Assurance")

        titles = qa_open_positions_page.get_position_titles()
        logging.debug("Position titles: \n{titles}".format(titles=titles))
        for title in titles:
            assert_that("quality assurance" in title.lower() or "qa" in title.lower()).is_true()

        locations = qa_open_positions_page.get_position_locations()
        logging.debug("Position locations: \n{locations}".format(locations=locations))
        for location in locations:
            assert_that(location).is_equal_to("Istanbul, Turkey")

        departments = qa_open_positions_page.get_position_departments()
        logging.debug("Position departments: \n{departments}".format(departments=departments))
        for department in departments:
            assert_that(department).is_equal_to("Quality Assurance")

        qa_open_positions_page.verify_apply_button_exists()

        #  click to first position in list
        position_to_apply = titles[0]
        qa_open_positions_page.click_apply_to_of_position(position_to_apply)
        web_browser.switch_to.window(web_browser.window_handles[1])
        application_form_page = LeverApplicationFormPage(web_browser)
        assert_that(application_form_page.get_position_title()).is_equal_to_ignoring_case(position_to_apply)
