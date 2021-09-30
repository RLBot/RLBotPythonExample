import math

from rlbot.utils.structures.game_data_struct import PlayerInfo

from util.orientation import Orientation, relative_location
from rlbot.utils.structures.ball_prediction_struct import BallPrediction
from util.ball_prediction_analysis import find_slice_at_time
from util.vec import Vec3


def limit_to_safe_range(value: float) -> float:
    """
    Controls like throttle, steer, pitch, yaw, and roll need to be in the range of -1 to 1.
    This will ensure your number is in that range. Something like 0.45 will stay as it is,
    but a value of -5.6 would be changed to -1.
    """
    if value < -1:
        return -1
    if value > 1:
        return 1
    return value

def get_horizontal_angle(car: PlayerInfo, target: Vec3) -> float:
    relative = relative_location(Vec3(car.physics.location), Orientation(car.physics.rotation), target)
    return math.atan2(relative.y, relative.x)

def get_vertical_angle(car: PlayerInfo, target: Vec3) -> float:
    relative = relative_location(Vec3(car.physics.location), Orientation(car.physics.rotation), target)
    adjacent = relative.flat().length()
    hypotenuse = relative.length()
    return math.acos(adjacent / hypotenuse)

def steer_toward_target(car: PlayerInfo, target: Vec3) -> float:
    return limit_to_safe_range(angle_to_target(car,target) * 5)

def steer_toward_target(angle: float) -> float:
    return limit_to_safe_range(angle * 5)

def get_eta(car: Vec3,car_v: Vec3, target: Vec3) -> float:
    distance = car.dist(target)
    velocity = car_v.length() if car_v.length() else 0.01
    return distance / velocity

def get_eta_ball(car: Vec3, car_v: Vec3, prediction: BallPrediction, initial_time: float) -> float:

    ball_slice = find_slice_at_time(prediction, initial_time)
    if not ball_slice:
        return 99.9

    ball_pos = ball_slice.physics.location
    eta = get_eta(car, car_v, ball_pos)

    time = initial_time
    delta = 99.9

    #####

    while abs(delta) < 0.1:
        time = time + eta

        ball_slice = find_slice_at_time(prediction, time)
        if not ball_slice:
            return eta

        ball_pos = ball_slice.physics.location
        new_eta = get_eta(car, car_v, ball_pos)


        delta = new_eta - eta
        eta = new_eta

    return eta
