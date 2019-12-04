import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3


class MyBot(BaseAgent):

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)
        ball_location = Vec3(packet.game_ball.physics.location)

        # Numbers taken from https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
        enemy_goal_y_value = 5200 if my_car.team == 0 else -5200
        enemy_goal_location = Vec3(0, enemy_goal_y_value, 0)

        target = ball_location

        controller_state = SimpleControllerState()
        controller_state.throttle = 1.0  # Positive throttle drives forward, negative drives backward
        controller_state.steer = steer_toward_target(my_car, target)

        # controller_state.boost = True  # Use boost to go fast or fly
        # controller_state.use_item = True  # Use item to retract your spikes and release the ball
        # controller_state.handbrake = True  # Use the handbrake to slide and turn sharply
        # controller_state.jump = True  # The car will jump when this *transitions* from False to True

        # These tilt the car when it's in mid-air
        # controller_state.pitch = 0.0
        # controller_state.yaw = 0.0
        # controller_state.roll = 0.0

        return controller_state

    def initialize_agent(self):
        # This runs once before the bot starts up
        pass


def steer_toward_target(my_car, target):
    car_location = Vec3(my_car.physics.location)
    car_to_target = target - car_location
    car_orientation = Orientation(my_car.physics.rotation)
    car_direction = car_orientation.forward
    steer_correction_radians = find_correction(car_direction, car_to_target)
    # A negative steer value turns the car left, which happens to be positive radians, so we invert
    # the value here. Also multiplying by a constant to steer more sharply. Max range for steering is -1 to 1.
    return clamp(-4 * steer_correction_radians, -1.0, 1.0)


def clamp(value, minimum, maximum):
    if value > maximum:
        return maximum
    if value < minimum:
        return minimum
    return value


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
