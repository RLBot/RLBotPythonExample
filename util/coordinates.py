from RLUtilities.LinearAlgebra import vec3, norm
import math

PI = math.pi


def spherical(vec: vec3) -> vec3:
    """Converts from cartesian to spherical coordinates."""
    radius = norm(vec) + 1e-9
    inclination = math.acos(vec[2] / radius)
    azimuth = math.atan2(vec[1], vec[0])
    return vec3(radius, Range180(PI / 2 - inclination), azimuth)


def Range180(a: float, pi: float = PI) -> float:
    """Limits any angle a to [-pi, pi] range, example: Range180(270, 180) = -90"""
    if abs(a) >= 2 * pi:
        a -= abs(a) // (2 * pi) * 2 * pi * math.copysign(1, a)
    if abs(a) > pi:
        a -= 2 * pi * math.copysign(1, a)
    return a
