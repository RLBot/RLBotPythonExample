from rlbot.agents.base_agent import SimpleControllerState
from RLUtilities.GameInfo import GameInfo


class BaseAction:

    def __init__(self, renderer):
        self.controls = SimpleControllerState()
        self.renderer = renderer
        self.finished = False
        self.failed = False

    def get_output(self, info: GameInfo) -> SimpleControllerState:
        raise NotImplementedError

    def get_possible(self, info: GameInfo) -> bool:
        raise NotImplementedError

    def update_status(self, info: GameInfo) -> bool:
        raise NotImplementedError

    def reset_status(self):
        self.finished = False
        self.failed = False
