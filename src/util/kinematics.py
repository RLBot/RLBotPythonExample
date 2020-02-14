
from __future__ import annotations

import math
import os
import sys

from util.constants import INV_BOOST_CONSUMPTION_RATE, TOP_DRIVE_VEL, BOOST_CONSUMPTION_RATE

from typing import List

epsilon = sys.float_info.epsilon


def sign(n: float) -> float:
    return -1 if n < 0 else 1


def not_zero(n: float) -> float:
    return n if abs(n) > epsilon else epsilon * sign(n)


# A single point of a loop-up table.
class AccelerationModelPoint:
    def __init__(self, time: float, velocity: float, position: float):
        self.time = time
        self.velocity = velocity
        self.position = position

    def copy(self) -> AccelerationModelPoint:
        return AccelerationModelPoint(self.time, self.velocity, self.position)

    @staticmethod
    def create(line: str) -> AccelerationModelPoint:
        nums = line.split(",")
        return AccelerationModelPoint(float(nums[0]), float(nums[1]), float(nums[2]))


# Creates a lookup table from a file.
def create_lut(file_name: str) -> List[AccelerationModelPoint]:
    cwd = os.getcwd()
    _path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(_path)

    lut_f = open(file_name, "r")
    lut = []
    for line in lut_f.readlines():
        if len(line) > 0:
            a = AccelerationModelPoint.create(line)
            lut.append(a)

    os.chdir(cwd)

    return lut


# Binary search time
def get_time(arr: List[AccelerationModelPoint], val: float, s: int = 0, e: int = -1) -> AccelerationModelPoint:
    if e < 0:
        e = len(arr)
    length = e - s
    div = s + int(length * 0.5)
    if length == 1:
        return arr[div]
    elif arr[div].time > val:
        return get_time(arr, val, s, div)
    else:
        return get_time(arr, val, div, e)


# Binary search velocity
def get_velocity(arr: List[AccelerationModelPoint], val: float, s: int = 0, e: int = -1) -> AccelerationModelPoint:
    if e < 0:
        e = len(arr)
    length = e - s
    div = s + math.floor(length * 0.5)
    if length == 1:
        return arr[div]
    elif arr[div].velocity > val:
        return get_velocity(arr, val, s, div)
    else:
        return get_velocity(arr, val, div, e)


# Binary search position
def get_position(arr: List[AccelerationModelPoint], val: float, s: int = 0, e: int = -1) -> AccelerationModelPoint:
    if e < 0:
        e = len(arr)
    length = e - s
    div = s + math.floor(length * 0.5)
    if length == 1:
        return arr[div]
    elif arr[div].position > val:
        return get_position(arr, val, s, div)
    else:
        return get_position(arr, val, div, e)


# Lookup tables. I could have put these in constants, but that would create some awkward imports.
ACCELERATION_LUT = create_lut("util/acceleration.txt")
BOOST_ACCELERATION_LUT = create_lut("util/boost_acceleration.txt")


# Returned by Kinematics1D functions.
class DriveManeuver:
    def __init__(self, dist: float, vel: float, time: float, boost: float):
        self.distance = dist
        self.velocity = vel
        self.time = time
        self.boost = boost


DriveManeuver.failed = DriveManeuver(0, 0, 0, 0)


# Simple drive without flips or wave dashes.
# PLEASE DO NOT ASK ME HOW THIS WORKS! I DON'T HAVE THE BRAIN SPACE TO ACTUALLY FIGURE IT OUT AND I DON'T REMEMBER WHAT
# I WAS THINKING AT THE TIME I WROTE THIS!
class Kinematics1D:

    @staticmethod
    def from_length(length: float, initial_v: float = 0, boost: float = 0) -> DriveManeuver:
        no_boost_time = boost * INV_BOOST_CONSUMPTION_RATE
        initial_conditions = get_velocity(BOOST_ACCELERATION_LUT, initial_v)
        no_boost = get_time(BOOST_ACCELERATION_LUT, initial_conditions.time + no_boost_time)

        # assume we have boost the entire time
        end_loc_1 = get_position(BOOST_ACCELERATION_LUT, initial_conditions.position + length)

        if end_loc_1.time > no_boost.time:
            if no_boost.velocity > TOP_DRIVE_VEL:
                extra_time = (length - (no_boost.position - initial_conditions.position)) / no_boost.velocity
                return DriveManeuver(length, no_boost.velocity, no_boost.time + extra_time, boost)
            else:
                initial_no_boost = get_velocity(ACCELERATION_LUT, no_boost.velocity)
                final_no_boost = get_position(ACCELERATION_LUT, initial_no_boost.position + length - (
                            no_boost.position - initial_conditions.position))

                return DriveManeuver(length, final_no_boost.velocity, no_boost.time - initial_conditions.time
                                     + initial_no_boost.time - final_no_boost.time, boost)
        else:
            extra_time = (length - (end_loc_1.position - initial_conditions.position)) / not_zero(end_loc_1.velocity)
            time = end_loc_1.time - initial_conditions.time
            return DriveManeuver(length, end_loc_1.velocity, time + extra_time, time * BOOST_CONSUMPTION_RATE)

    @staticmethod
    def from_velocity(vel: float, initial_v: float = 0, boost: float = 0) -> DriveManeuver:
        no_boost_time = boost * INV_BOOST_CONSUMPTION_RATE
        initial_conditions = get_velocity(BOOST_ACCELERATION_LUT, initial_v)
        no_boost = get_time(BOOST_ACCELERATION_LUT, initial_conditions.time + no_boost_time)

        end_loc_1 = get_velocity(BOOST_ACCELERATION_LUT, vel)

        if end_loc_1.time > no_boost.time:
            if vel > TOP_DRIVE_VEL:
                return DriveManeuver.failed
            else:
                start_loc_2 = get_velocity(ACCELERATION_LUT, no_boost.velocity)
                end_loc_2 = get_velocity(ACCELERATION_LUT, vel)
                length = end_loc_1.position - initial_conditions.position + end_loc_2.position - start_loc_2.position
                time = end_loc_1.time - initial_conditions.time + end_loc_2.time - start_loc_2.time
                return DriveManeuver(length, vel, time, boost)
        else:
            time = end_loc_1.time - initial_conditions.time
            return DriveManeuver(end_loc_1.position - initial_conditions.position, vel, time,
                                 time * BOOST_CONSUMPTION_RATE)

    @staticmethod
    def from_time(time: float, initial_v: float = 0, boost: float = 0) -> DriveManeuver:

        initial_conditions = get_velocity(BOOST_ACCELERATION_LUT, initial_v)

        no_boost_time = boost * INV_BOOST_CONSUMPTION_RATE

        no_boost = get_time(BOOST_ACCELERATION_LUT, initial_conditions.time + no_boost_time)

        if no_boost.velocity > TOP_DRIVE_VEL:
            extra = no_boost.velocity * (time - (no_boost.time - initial_conditions.time))
            return DriveManeuver(no_boost.position - initial_conditions.position + extra, no_boost.velocity,
                                 time, (no_boost.time - initial_conditions.time) * BOOST_CONSUMPTION_RATE)
        else:
            start_loc_2 = get_velocity(ACCELERATION_LUT, no_boost.velocity)
            end_loc_2 = get_time(
                ACCELERATION_LUT, start_loc_2.time + time - (no_boost.time - initial_conditions.time))
            length = (
                no_boost.position - initial_conditions.position + end_loc_2.position - start_loc_2.position)

            time_taken = (end_loc_2.time - start_loc_2.time + no_boost.time - initial_conditions.time)
            extra = end_loc_2.velocity * (time - time_taken)

            return DriveManeuver(length + extra, end_loc_2.velocity, time, boost)
