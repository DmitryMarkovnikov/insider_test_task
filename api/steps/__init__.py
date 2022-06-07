from api.steps.pets_steps import PetsApiSteps


class PetsAPI:
    def __init__(self, session=None):
        self.session = session
        self.pets_steps = PetsApiSteps(session=self.session)
