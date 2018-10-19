import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3


class PythonExample(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        ball_location = Vec3().set(packet.game_ball.physics.location)

        # Let's find the direction to the ball
        my_car = packet.game_cars[self.index]
        car_location = Vec3().set(my_car.physics.location)
        car_to_ball = ball_location - car_location

        # Let's find the direction of our car
        car_orientation = Orientation(my_car.physics.rotation)  # This handy class can tell us the direction of our car
        car_direction = car_orientation.forward

        # Now we find how much we are off
        steer_correction_radians = car_direction.ang_to_2d(car_to_ball)

        # Do we need to turn left or right?
        if steer_correction_radians > 0:
            turn = 1.0
        else:
            turn = -1.0

        self.controller_state.throttle = 1.0
        self.controller_state.steer = turn

        return self.controller_state
