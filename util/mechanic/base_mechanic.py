from rlbot.agents.base_agent import SimpleControllerState


class BaseMechanic:

    def __init__(self):
        self.controls = SimpleControllerState()

    def step(self, dt: float = 0.1667) -> SimpleControllerState:
        raise NotImplementedError
