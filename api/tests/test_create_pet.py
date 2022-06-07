import pytest
from assertpy import assert_that, soft_assertions
from requests import codes

from api.models import Pet


class TestCreatePet:

    def test_create_pet_ok(self, unauthorized_pets_api):
        pet = Pet()
        resp = unauthorized_pets_api.pets_steps.create_pet(pet)

        with soft_assertions():
            assert_that(resp["category"]).is_equal_to(pet.category)
            assert_that(resp["name"]).is_equal_to(pet.name)
            assert_that(resp["photoUrls"]).is_equal_to(pet.photoUrls)
            assert_that(resp["tags"]).is_equal_to(pet.tags)
            assert_that(resp["status"]).is_equal_to(pet.status)

    missing_test_data = [
        (
            Pet(category=None),
            "category"
        ),
        (
            Pet(name=None),
            "name"
        ),
        (
            Pet(photoUrls=None),
            "photoUrls"
        ),
        (
            Pet(tags=None),
            "tags"
        ),
        (
            Pet(status=None),
            "status"
        )
    ]

    @pytest.mark.parametrize("pet,key", missing_test_data)
    def test_create_pet_with_missing_data_ok(self, unauthorized_pets_api, pet, key):
        resp = unauthorized_pets_api.pets_steps.create_pet(pet)
        assert_that(resp).does_not_contain_key(key)

    corrupted_test_data = [
        Pet(category={"dummy_key": 1, "name": "pet_category"}),
        Pet(category={"id": 1, "dummy_key": 1}),
        Pet(tags=[{"dummy_string": 1, "name": "pet_name"}]),
        Pet(tags=[{"id": 1, "dummy_string": 1}]),
        Pet(photoUrls=[1, 2, 3]),
        Pet(status=1),
    ]

    @pytest.mark.parametrize("pet", corrupted_test_data)
    def test_create_pet_with_corrupted_data(self, unauthorized_pets_api, pet):
        unauthorized_pets_api.pets_steps.create_pet(pet)

    invalid_test_data = [
        pytest.param(
            Pet(id="dummy_string"),
            codes.bad,
            marks=pytest.mark.xfail(reason="INTERNAL SERVER ERROR")
        ),
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
    def test_create_pet_with_invalid_data_not_ok(self, unauthorized_pets_api, pet, code):
        unauthorized_pets_api.pets_steps.create_pet(pet, expected_code=code)
