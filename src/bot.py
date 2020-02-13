import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3
from util.sequence import Sequence, ControlStep


class MyBot(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.active_sequence: Sequence = None

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        if self.active_sequence and not self.active_sequence.done:
            return self.active_sequence.tick(packet)

        ball_location = Vec3(packet.game_ball.physics.location)
        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)
        car_velocity = Vec3(my_car.physics.velocity)

        if 550 < car_velocity.length() < 600:
            self.active_sequence = Sequence([
                ControlStep(0.05, SimpleControllerState(jump=True)),
                ControlStep(0.05, SimpleControllerState(jump=False)),
                ControlStep(0.2, SimpleControllerState(jump=True, pitch=-1)),
                ControlStep(0.8, SimpleControllerState()),
            ])
            return self.active_sequence.tick(packet)

        car_to_ball = ball_location - car_location

        # Find the direction of our car using the Orientation class
        car_orientation = Orientation(my_car.physics.rotation)
        car_direction = car_orientation.forward

        steer_correction_radians = find_correction(car_direction, car_to_ball)

        self.controller_state.throttle = 1.0
        self.controller_state.steer = -1 if steer_correction_radians > 0 else 1.0

        return self.controller_state


def find_correction(current: Vec3, ideal: Vec3) -> float:
    # Finds the angle from current to ideal vector in the xy-plane. Angle will be between -pi and +pi.

    # The in-game axes are left handed, so use -x
    current_in_radians = math.atan2(current.y, -current.x)
    ideal_in_radians = math.atan2(ideal.y, -ideal.x)

    diff = ideal_in_radians - current_in_radians

    # Make sure that diff is between -pi and +pi.
    if abs(diff) > math.pi:
        if diff < 0:
            diff += 2 * math.pi
        else:
            diff -= 2 * math.pi

    return diff
