import math

from action.base_action import BaseAction
from rlbot.agents.base_agent import SimpleControllerState

from RLUtilities.GameInfo import GameInfo
from RLUtilities.LinearAlgebra import dot, norm


class Kickoff(BaseAction):

    def get_output(self, info: GameInfo) -> SimpleControllerState:

        ball = info.ball
        car = info.my_car

        local_coords = dot(ball.pos - car.pos, car.theta)

        self.controls.steer = math.copysign(1.0, local_coords[1])

        # just set the throttle to 1 so the car is always moving forward
        self.controls.throttle = 1.0

        return self.controls

    def get_possible(self, info: GameInfo):
        return True

    def update_status(self, info: GameInfo):

        if norm(info.ball.pos) > 140 and norm(info.ball.vel) > 9:  # this only works for soccar

            if norm(info.ball.pos - info.my_car.pos) < 240:
                self.finished = True
            else:
                self.failed = True
