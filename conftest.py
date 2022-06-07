import logging

import pytest

logging.getLogger("logger").setLevel(logging.ERROR)

pytest_plugins = ["conftest_ui", "conftest_api"]


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    This function helps to detect that some test failed and pass this information to teardown:
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep
