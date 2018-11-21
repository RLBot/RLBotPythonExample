from action.base_test_agent import BaseTestAgent
from action.collect_boost.collect_boost import CollectBoost
from rlbot.utils.game_state_util import GameState, CarState, Physics, Vector3, Rotator
from rlbot.utils.structures.game_data_struct import GameTickPacket

import math
import random


class TestAgent(BaseTestAgent):
    initialization_time = -1
    timeout = 5

    def test_process(self, game_tick_packet: GameTickPacket):
        self.action.update_status(self.info)

        if self.info.time > self.initialization_time + self.timeout or self.action.finished:

            log_message = "Finished" if self.action.finished else "Timed out"
            log_message = log_message + ". Took " + str(self.info.time - self.initialization_time) + " Seconds."
            self.logger.info(log_message)

            self.initialize_agent()

    def initialize_agent(self):

        random_position = Vector3(random.uniform(-3000, 3000), random.uniform(-4000, 4000), 18)
        random_velocity = Vector3(random.uniform(-1000, 1000), random.uniform(-1000, 1000), 0)
        random_rotation = Rotator(0, random.uniform(-math.pi, math.pi), 0)

        car_physics = Physics(location=random_position, velocity=random_velocity, rotation=random_rotation,
                              angular_velocity=Vector3(0, 0, 0))

        boost = random.uniform(0, 50)

        car_state = CarState(boost_amount=boost, physics=car_physics)

        game_state = GameState(cars={self.index: car_state})

        self.set_game_state(game_state)

        self.initialization_time = self.info.time
        self.action.reset_status()

    def create_action(self):
        return CollectBoost(self.renderer)
