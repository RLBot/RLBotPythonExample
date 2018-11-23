from util.mechanic.base_test_agent import BaseTestAgent
from util.mechanic.aerial_turn.face_vector import FaceVector
from rlbot.utils.game_state_util import GameState, CarState, BallState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket

import math
import random

random.seed(0)


class TestAgent(BaseTestAgent):
    initialization_time = -1
    timeout = 2

    def test_process(self, game_tick_packet: GameTickPacket):

        self.car_physics = Physics(velocity=Vector3(0, 0, 10))
        self.ball_state = BallState(physics=Physics(velocity=Vector3(0, 0, 10), location=Vector3(0, 0, 800)))

        if self.info.time > self.initialization_time + self.timeout:
            self.initialize_agent()

        self.set_game_state(GameState(cars={self.index: CarState(physics=self.car_physics)}, ball=self.ball_state))

    def initialize_agent(self):

        if not hasattr(self, 'car_physics'):
            self.car_physics = Physics()

        self.car_physics.rotation = Rotator(random.uniform(-math.pi / 2, math.pi / 2),
                                            random.uniform(-math.pi, math.pi), random.uniform(-math.pi, math.pi))
        self.car_physics.location = Vector3(random.uniform(-1000, 1000),
                                            random.uniform(-1000, 1000), random.uniform(50, 1400))
        self.car_physics.angular_velocity = Vector3(random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5))

        self.ball_state = BallState(physics=Physics(velocity=Vector3(0, 0, 10), location=Vector3(0, 0, 800)))

        self.initialization_time = self.info.time

    def get_mechanic_controls(self):
        target = self.info.ball.pos - self.info.my_car.pos
        return FaceVector(self.info.my_car, target).step(0.01667)
