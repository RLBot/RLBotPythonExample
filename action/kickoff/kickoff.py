import math

from action.base_action import BaseAction
from rlbot.agents.base_agent import SimpleControllerState

from RLUtilities.GameInfo import GameInfo
from RLUtilities.Simulation import Car, Ball
from RLUtilities.LinearAlgebra import vec3, dot, clip, norm


class TouchInfo:
    ball = Ball()
    time = -1


class Kickoff(BaseAction):
    def get_output(self, info: GameInfo) -> SimpleControllerState:

        ball = info.ball
        car = info.my_car

        local_coords = dot(ball.pos - car.pos, car.theta)

        self.controls.steer = math.copysign(1.0, local_coords[1])

        # just set the throttle to 1 so the car is always moving forward
        self.controls.throttle = 1.0

        return self.controls

    def get_next_touch(self, info: GameInfo) -> TouchInfo:
        return TouchInfo()

    def get_car_at_time(self, info: GameInfo, time: float) -> Car:
        return Car()

    def update_status(self, info: GameInfo) -> bool:

        if norm(info.ball.pos) > 140 and norm(info.ball.vel) > 9:  # this only works for soccar

            if norm(info.ball.pos - info.my_car.pos) < 240:
                self.finished = True
            else:
                self.failed = True

    def reset_status(self):
        self.finished = False
        self.failed = False
