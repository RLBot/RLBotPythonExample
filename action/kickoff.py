

import math

from .base_action import BaseAction
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from RLUtilities.GameInfo import GameInfo
from RLUtilities.Simulation import Car, Ball
from RLUtilities.LinearAlgebra import vec3, dot, clip

from RLUtilities.controller_input import controller


class TouchInfo:
    ball = Ball()
    time = -1


class Kickoff(BaseAction):

    def __init__(self, renderer):
        self.controls = SimpleControllerState()
        self.renderer = renderer

    def get_output(self, info: GameInfo) -> SimpleControllerState:

        ball = info.ball
        car = info.my_car

        steer_left = dot(ball.pos - car.pos, car.theta[1])

        self.controls.steer = math.copysign(steer_left, 1.0)

        # just set the throttle to 1 so the car is always moving forward
        self.controls.throttle = 1.0

        return self.controls

    def get_next_touch(self, info: GameInfo) -> TouchInfo:
        return TouchInfo()

    def get_car_at_time(self, info: GameInfo, time: float) -> Car:
        return Car()
