from action.base_action import BaseAction
from util.boost_utils import closest_available_boost
from rlbot.agents.base_agent import SimpleControllerState

from RLUtilities.Maneuvers import Drive
from RLUtilities.GameInfo import GameInfo


class CollectBoost(BaseAction):

    def get_output(self, info: GameInfo) -> SimpleControllerState:

        car = info.my_car
        boost_pad = closest_available_boost(car.pos, info.boost_pads)

        if boost_pad is None:
            # All boost pads are inactive.
            return self.controls

        self.action = Drive(car, boost_pad.pos, 2310)

        self.action.step(0.01666)
        self.controls = self.action.controls

        return self.controls

    def get_possible(self, info: GameInfo):
        return True

    def update_status(self, info: GameInfo):
        if info.my_car.boost == 100:
            self.finished = True
