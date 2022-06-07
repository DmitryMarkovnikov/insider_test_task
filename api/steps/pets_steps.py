from dataclasses import asdict

import allure
from requests import codes

from api.http_manager import HttpManager
from api.steps.base_api_steps import BaseApiSteps
from settings import api_settings


class PetsApiSteps(BaseApiSteps):

    _url_get_pet = "pet/{pet_id}"
    _url_create_pet = "pet"
    _url_delete_pet = "pet/{pet_id}"
    _url_update_pet = "pet"

    def __init__(self, base_url=api_settings.base_api_url, session=None):
        super().__init__(base_url, session)

    @allure.step
    def get_pet(self, pet_id,
                expected_status_code=codes.ok):

        req = HttpManager.get(self._url_get_pet.format(pet_id=pet_id))

        resp = self.call_with_log(req, return_json=True, expected_status_code=expected_status_code)
        return resp

    @allure.step
    def create_pet(self, pet_obj, expected_status_code=codes.ok):
        req = HttpManager.post_json(self._url_create_pet, data=asdict(pet_obj))

        resp_json = self.call_with_log(req, return_json=True, expected_status_code=expected_status_code)
        return resp_json

    @allure.step
    def delete_pet(self,
                   pet_id,
                   return_json=True,
                   expected_status_code=codes.ok):

        req = HttpManager.delete(self._url_delete_pet.format(pet_id=pet_id))

        resp = self.call_with_log(req, return_json=return_json, expected_status_code=expected_status_code)
        return resp

    @allure.step
    def update_pet(self, pet_obj,
                   return_json=True,
                   expected_status_code=codes.ok):

        req = HttpManager.put_json(self._url_update_pet, data=asdict(pet_obj))

        resp = self.call_with_log(req, return_json=return_json, expected_status_code=expected_status_code)
        return resp
