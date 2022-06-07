import pytest

from api.models import Pet
from api.steps import PetsAPI


@pytest.fixture(scope="module")
def unauthorized_pets_api():
    """
    """
    return PetsAPI()


@pytest.fixture
def created_pet(unauthorized_pets_api):
    pet = Pet()
    created_pet_resp = unauthorized_pets_api.pets_steps.create_pet(pet)
    return Pet(**created_pet_resp)
