from rlbottraining.rng import SeededRandomNumberGenerator

from rlbot.utils.game_state_util import Vector3


def get_car_start_near_goal(rng: SeededRandomNumberGenerator) -> Vector3:
    return Vector3(rng.uniform(1000, 2000), 3000, 0)
