from RLUtilities.GameInfo import BoostPad
from RLUtilities.LinearAlgebra import vec3, norm


def closest_available_boost(my_pos: vec3, boost_pads: list) -> BoostPad:
    """ Returns the closest available boost pad to my_pos"""
    closest_boost = None
    for boost in boost_pads:
        distance = norm(boost.pos - my_pos)
        if boost.is_active or distance / 2300 > 10 - boost.timer:
            if closest_boost is None:
                closest_boost = boost
                closest_distance = norm(closest_boost.pos - my_pos)
            else:
                if distance < closest_distance:
                    closest_boost = boost
                    closest_distance = norm(closest_boost.pos - my_pos)
    return closest_boost
