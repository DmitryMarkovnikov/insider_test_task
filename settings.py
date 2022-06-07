import os

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    root_dir: str = os.path.dirname(os.path.abspath(__file__))


class UIProjectSettings(ProjectSettings):
    base_ui_url: str = "https://useinsider.com/"
    careers_url: str = "https://useinsider.com/careers/"
    root_dir: str = os.path.dirname(os.path.abspath(__file__))
    screenshot_path: str = "{root_dir}/ui/screenshots/".format(root_dir=root_dir)


class APIProjectSettings(ProjectSettings):
    base_api_url: str = "https://petstore.swagger.io/v2/"
    not_existing_pet_id = 10000


ui_settings = UIProjectSettings()
api_settings = APIProjectSettings()

if not os.path.exists(ui_settings.screenshot_path):
    os.makedirs(ui_settings.screenshot_path)
