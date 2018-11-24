from RLUtilities.LinearAlgebra import vec3, norm, mat3
import math


PI = math.pi


def spherical(vec: vec3) -> vec3:
    """Converts from cartesian to spherical coordinates."""
    radius = norm(vec) + 1e-9
    inclination = math.acos(vec[2] / radius)
    azimuth = math.atan2(vec[1], vec[0])
    return vec3(radius, Range180(PI / 2 - inclination), azimuth)


def pitch_point(ang: float, angvel: float) -> float:
    """PD pitch to point"""
    return sign(Range180(ang + angvel * pfs(angvel), PI)) * Range(abs(ang) + abs(angvel) * 2, 1)


def yaw_point(ang: float, angvel: float) -> float:
    """PD yaw to point"""
    return sign(Range180(ang - angvel * yfs(angvel), PI)) * Range(abs(ang) + abs(angvel) * 2, 1)


def roll_point(ang: float, angvel: float) -> float:
    """PD roll to point"""
    return sign(Range180(ang + angvel * rfs(angvel), PI)) * Range(abs(ang) / 2 + abs(angvel) / 2, 1)


def pfs(pitchspeed: float) -> float:
    """time until pitch full stop"""
    return abs(pitchspeed) / 25 + 1 / 13


def yfs(yawspeed: float) -> float:
    """time until yaw full stop"""
    return abs(yawspeed) / 20 + 1 / 10


def rfs(rollspeed: float) -> float:
    """time until roll full stop"""
    return abs(rollspeed) / 30 + 1 / 20


def Range(value: float, max_value: float = 1) -> float:
    """Constrains value to [-max_value, max_value] range"""
    if abs(value) > max_value:
        value = math.copysign(max_value, value)
    return value


def Range180(a: float, pi: float = PI) -> float:
    """Limits any angle a to [-pi, pi] range, example: Range180(270, 180) = -90"""
    if abs(a) >= 2 * pi:
        a -= abs(a) // (2 * pi) * 2 * pi * sign(a)
    if abs(a) > pi:
        a -= 2 * pi * sign(a)
    return a


def sign(x: float) -> float:
    """Retuns 1 if x > 0 else -1. > instead of >= so that sign(False) returns -1"""
    return 1 if x > 0 else -1


def rotationMatrixToEulerAngles(R: mat3) -> vec3:

    sy = math.sqrt(R[0, 0]**2 + R[1, 0]**2)

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return vec3(x, y, z)
