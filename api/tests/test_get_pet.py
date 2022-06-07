import pytest
from assertpy import soft_assertions, assert_that
from requests import codes

import settings


class TestGetPet:

    def test_get_pet_ok(self, unauthorized_pets_api, created_pet):
        resp = unauthorized_pets_api.pets_steps.get_pet(created_pet.id)
        with soft_assertions():
            assert_that(resp["category"]).is_equal_to(created_pet.category)
            assert_that(resp["name"]).is_equal_to(created_pet.name)
            assert_that(resp["photoUrls"]).is_equal_to(created_pet.photoUrls)
            assert_that(resp["tags"]).is_equal_to(created_pet.tags)
            assert_that(resp["status"]).is_equal_to(created_pet.status)

    def test_get_not_existing_pet_ok(self, unauthorized_pets_api):
        resp = unauthorized_pets_api.pets_steps.get_pet(settings.api_settings.not_existing_pet_id,
                                                        expected_status_code=codes.not_found)
        assert_that(resp).has_code(1)
        assert_that(resp).has_type("error")
        assert_that(resp).has_message("Pet not found")

    invalid_test_data = [
        (
            "dummy_string",
            codes.bad
         ),
    ]

    @pytest.mark.parametrize("param,code", invalid_test_data)
    def test_get_pet_with_invalid_data(self, unauthorized_pets_api, param, code):
        unauthorized_pets_api.pets_steps.get_pet(param, expected_status_code=codes)


