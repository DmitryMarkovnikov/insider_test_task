import pytest
from assertpy import assert_that
from requests import codes

from api.models import Pet


class TestUpdatePet:
    test_data = [
        ({"name": "updated_pet"}),
        ({"category": {"id": 1, "name": "updated_category"}}),
        ({"photoUrls": ["url1", "url2"]}),
        ({"tags":  [{"id": 1, "name": "updated_tag"}]}),
        ({"status": "not available"})
    ]

    @pytest.mark.parametrize("test_data", test_data)
    def test_update_pet_ok(self, unauthorized_pets_api, created_pet, test_data):

        data = {"id": created_pet.id}
        data.update(test_data)
        pet = Pet(**data)
        updated_value = list(test_data.keys())[0]
        resp = unauthorized_pets_api.pets_steps.update_pet(pet)
        assert_that(resp[updated_value]).is_equal_to(pet.__getattribute__(updated_value))
        assert_that(resp[updated_value]).is_not_equal_to(created_pet.__getattribute__(updated_value))

    def test_update_not_existing_pet_ok(self, unauthorized_pets_api):
        """
        Will create new pet if there is no existing id
        """
        pet = Pet(name="updated_not_existing")
        resp = unauthorized_pets_api.pets_steps.update_pet(pet)
        assert_that(resp["name"]).is_equal_to(pet.name)

    invalid_test_data = [
        pytest.param(
            Pet(category=1),
            codes.bad,
            marks=pytest.mark.xfail(reason="INTERNAL SERVER ERROR")
        ),
        pytest.param(
            Pet(category="dummy_string"),
            codes.bad,
            marks=pytest.mark.xfail(reason="INTERNAL SERVER ERROR")
        ),
        pytest.param(
            Pet(tags=1),
            codes.bad,
            marks=pytest.mark.xfail(reason="INTERNAL SERVER ERROR")
        ),
        pytest.param(
            Pet(tags="dummy_string"),
            codes.bad,
            marks=pytest.mark.xfail(reason="INTERNAL SERVER ERROR")
        ),
        pytest.param(
            Pet(tags={"id": 1, "name": "pet_tag"}),
            codes.bad,
            marks=pytest.mark.xfail(reason="INTERNAL SERVER ERROR")
        ),
        pytest.param(
            Pet(photoUrls="dummy_string"),
            codes.bad,
            marks=pytest.mark.xfail(reason="INTERNAL SERVER ERROR")
        ),
    ]

    @pytest.mark.parametrize("pet,code", invalid_test_data)
    def test_update_pet_with_invalid_data(self, unauthorized_pets_api, created_pet, pet, code):
        pet.id = created_pet.id
        unauthorized_pets_api.pets_steps.update_pet(pet, expected_status_code=code)

