import pytest
from assertpy import assert_that, soft_assertions
from requests import codes

import settings


class TestDeletePet:
    def test_delete_pet_ok(self, unauthorized_pets_api, created_pet):
        resp = unauthorized_pets_api.pets_steps.delete_pet(created_pet.id)
        with soft_assertions():
            assert_that(resp).has_type('unknown')
            assert_that(resp).has_message(str(created_pet.id))
        unauthorized_pets_api.pets_steps.get_pet(created_pet.id, expected_status_code=codes.not_found)

    def test_delete_not_existing_pet_ok(self, unauthorized_pets_api):
        unauthorized_pets_api.pets_steps.delete_pet(settings.api_settings.not_existing_pet_id,
                                                    return_json=False,
                                                    expected_status_code=codes.not_found)

    invalid_test_data = [
        (
            "dummy_string",
            codes.bad
        ),
    ]

    @pytest.mark.parametrize("param,code", invalid_test_data)
    def test_get_pet_with_invalid_data(self, unauthorized_pets_api, param, code):
        unauthorized_pets_api.pets_steps.delete_pet(param, expected_status_code=codes)

