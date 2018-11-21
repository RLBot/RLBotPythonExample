from action.base_test_agent import BaseTestAgent
from action.kickoff.kickoff import Kickoff
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket

import math


class TestAgent(BaseTestAgent):
    flip = False
    diagonal = True
    initialization_time = -1
    timeout = 5

    def test_process(self, game_tick_packet: GameTickPacket):
        self.action.update_status(self.info)
        if self.info.time > self.initialization_time + self.timeout or self.action.finished or self.action.failed:
            self.initialize_agent()

    def initialize_agent(self):
        m = -1 if self.team else 1
        f = -1 if self.flip else 1

        if self.diagonal:
            car_physics = Physics(velocity=Vector3(0, 0, 0),
                                  rotation=Rotator(0, (45 + m * 90) / 180 * math.pi, 0),
                                  angular_velocity=Vector3(0, 0, 0),
                                  location=Vector3(f * m * 2048, m * -2560, 17.148628))

        ball_physics = Physics(location=Vector3(0, 0, 92.739998),
                               velocity=Vector3(0, 0, 0),
                               angular_velocity=Vector3(0, 0, 0),)

        car_state = CarState(jumped=False, double_jumped=False, boost_amount=34, physics=car_physics)

        ball_state = BallState(physics=ball_physics)

        game_state = GameState(ball=ball_state, cars={self.index: car_state})

        self.set_game_state(game_state)

        self.initialization_time = self.info.time

        self.action.reset_status()

    def create_action(self):
        return Kickoff(self.renderer)
