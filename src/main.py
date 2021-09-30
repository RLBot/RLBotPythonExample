from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.game_data_struct import GoalInfo

from util.ball_prediction_analysis import *
from util.boost_pad_tracker import BoostPadTracker
from util.drive import *
from util.sequence import Sequence, ControlStep
from util.vec import Vec3
from util.orientation import *

import math
from random import random
from typing import List

BALL_RADIUS = 92.75

# blue,   team0, negative y
# orange, team1, positive y


class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.active_sequence: Sequence = None
        self.boost_pad_tracker = BoostPadTracker()


    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        self.boost_pad_tracker.initialize_boosts(self.get_field_info())


    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        self.init(packet)

        self.draw_3d()
        self.draw_2d()

        return self.control(packet)

    def init(self, packet: GameTickPacket):
        self.boost_pad_tracker.update_boost_status(packet)

        self.car = packet.game_cars[self.index]
        self.car_location = Vec3(self.car.physics.location)
        self.car_velocity = Vec3(self.car.physics.velocity)
        self.car_rotation = Orientation(self.car.physics.rotation)

        self.ball = packet.game_ball
        self.ball_location = Vec3(self.ball.physics.location)
        self.ball_velocity = Vec3(self.ball.physics.velocity)

        self.goal_location = self.get_target_goal()

        self.time = packet.game_info.seconds_elapsed
        self.max_time = 2.0

        self.ball_prediction = self.get_ball_prediction_struct()
        self.ball_location_prediction = get_continuous_ball_prediction(self.ball_prediction, self.time, self.max_time)
        self.ball_eta = get_eta_ball(self.car_location, self.car_velocity, self.ball_prediction, self.time)

        if self.team == 1:
            self.color = self.renderer.orange()
        else:
            self.color = self.renderer.blue()

        self.target_location = self.get_target_prediction()

        self.horizontal_angle_to_target = get_horizontal_angle(self.car, self.target_location)
        self.vertical_angle_to_target = get_vertical_angle(self.car, self.target_location)

        self.distance_to_target = self.car_location.dist(self.target_location)

        self.target_eta = get_eta(self.car_location, self.car_velocity, self.target_location)


    def control(self, packet: GameTickPacket):

        if self.active_sequence is not None and not self.active_sequence.done:
            controls = self.active_sequence.tick(packet)
            if controls is not None:
                return controls

        if self.car_velocity.length() > 800 and (self.target_eta > 0.6 or self.target_eta < 0.1)and abs(self.horizontal_angle_to_target) < 0.1 and not self.car.double_jumped and self.car_location.z < 20:
            # We'll do a front flip if the car is moving at a certain speed.
            return self.begin_front_flip(packet)



        controls = SimpleControllerState()
        controls.steer = steer_toward_target(self.horizontal_angle_to_target)

        controls.throttle = limit_to_safe_range(0.3 / abs(self.vertical_angle_to_target))

        # if self.target_eta < 0.2 and self.car_velocity.length() > 500:
        #     controls.jump = True

        if self.car_velocity.length() < 1200:
            controls.boost = True

        if abs(self.horizontal_angle_to_target) > 2.0 :
            controls.handbrake = True

        # if self.car_location.z > 500.0 : #Wall jump
        #     controls.jump = True

        if self.car_rotation.forward.z > 0.1:
            controls.pitch = -0.5
        if self.car_rotation.forward.z < -0.1:
            controls.pitch = +0.5

        if self.car_rotation.right.z > 0.1:
            controls.roll = +0.5
        if self.car_rotation.right.z < -0.1:
            controls.roll = -0.5

        if self.horizontal_angle_to_target > 0.1:
            controls.yaw = +0.5
        if self.horizontal_angle_to_target < -0.1:
            controls.yaw = -0.5

        return controls

    def draw_3d(self):
        debug_string = f''

        self.renderer.draw_string_3d(self.car_location, 1, 1, debug_string, self.renderer.orange())
        self.renderer.draw_rect_3d(self.target_location, 8, 8, True, self.color, centered=True)
        self.renderer.draw_line_3d(self.car_location, self.target_location, self.renderer.white())
        self.renderer.draw_line_3d(self.ball_location, self.goal_location, self.color)

        if len(self.ball_location_prediction) > 2:
            self.renderer.draw_polyline_3d(self.ball_location_prediction, self.renderer.red())

    def draw_2d(self):
        x_offset = 50 if not self.team else 1500

        debug_string = f' spd: {self.car_velocity.length():.0f} \
            \n thr: {limit_to_safe_range(0.5 / self.vertical_angle_to_target):.2f} \
            \n anH: {self.horizontal_angle_to_target:.2f} \
            \n eta: {self.ball_eta:.2f}'


        self.renderer.draw_string_2d(
            x_offset, 50, 2, 2, debug_string, self.color)



    def get_target_goal(self) -> Vec3:
        for goal in self.get_field_info().goals:
            if goal.team_num != self.team:
                return Vec3(goal.location)

    def get_target_prediction(self) -> Vec3:

        ball_eta = min(self.ball_eta, self.max_time)

        prediction = get_single_ball_prediction(self.ball_prediction, self.time + ball_eta)

        if not prediction:
           return self.ball_location

        if ball_eta < 0.8:
            prediction = self.ball_location

        vector_ball_to_goal = self.goal_location - self.ball_location

        correction = vector_ball_to_goal.rescale(- BALL_RADIUS / 0.7)
        prediction = prediction + correction

        return prediction


    def begin_front_flip(self, packet):
        # Send some quickchat just for fun
        # self.send_quick_chat(team_only=False, quick_chat=QuickChatSelection.Information_IGotIt)

        # Do a front flip. We will be committed to this for a few seconds and the bot will ignore other
        # logic during that time because we are setting the active_sequence.
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, pitch=-1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        # Return the controls associated with the beginning of the sequence so we can start right away.
        return self.active_sequence.tick(packet)
