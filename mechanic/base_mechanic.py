from rlbot.agents.base_agent import SimpleControllerState


class BaseMechanic:

    def __init__(self):
        self.controls = SimpleControllerState()
        self.finished = False

    def step(self) -> SimpleControllerState:
        raise NotImplementedError
