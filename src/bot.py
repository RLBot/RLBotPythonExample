import math
from typing import List

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.quick_chats import QuickChats

from util.goal_detector import find_future_goal
from util.orientation import Orientation
from util.sequence import Sequence, ControlStep
from util.spikes import SpikeWatcher
from util.vec import Vec3

import numpy as np
from util.np_utils import a3v, closest_to

class MyBot(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.active_sequence: Sequence = None
        self.spike_watcher = SpikeWatcher()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        if self.active_sequence and not self.active_sequence.done:
            return self.active_sequence.tick(packet)

        self.spike_watcher.read_packet(packet)
        ball_prediction = self.get_ball_prediction_struct()

        # Example of predicting a goal event
        predicted_goal = find_future_goal(ball_prediction)
        goal_text = "No Goal Threats"
        if predicted_goal:
            goal_text = f"Goal in {predicted_goal.time - packet.game_info.seconds_elapsed:.2f}s"

        ball_location = Vec3(packet.game_ball.physics.location)
        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)
        car_velocity = Vec3(my_car.physics.velocity)

        # Example of using a sequence
        # This will do a front flip if the car's velocity is between 550 and 600
        if 550 < car_velocity.length() < 600:
            self.active_sequence = Sequence([
                ControlStep(0.05, SimpleControllerState(jump=True)),
                ControlStep(0.05, SimpleControllerState(jump=False)),
                ControlStep(0.2, SimpleControllerState(jump=True, pitch=-1)),
                ControlStep(0.8, SimpleControllerState()),
            ])
            return self.active_sequence.tick(packet)

        # Example of using the spike watcher.
        # This will make the bot say I got it! when it spikes the ball,
        # then release it 3 seconds later.
        if self.spike_watcher.carrying_car == my_car:
            if self.spike_watcher.carry_duration == 0:
                self.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Information_IGotIt)
            elif self.spike_watcher.carry_duration > 3:
                return SimpleControllerState(use_item=True)

        # Example to numpy utilities:
        # Get all car positions into an array.
        car_positions = []
        for car in packet.game_cars[:packet.num_cars]:
            car_positions.append(a3v(car.physics.location))
        car_positions_arr = np.vstack(car_positions)
        # Get the ball position.
        ball_pos = a3v(packet.game_ball.physics.location)
        # Find the closest car to the ball.
        closest_index = closest_to(ball_pos, car_positions_arr)
        # Prepare render message.
        closest_text = f'The bot with index {closest_index} is closest to the ball.'

        # The rest of this code just ball chases.
        # Find the direction of our car using the Orientation class
        car_orientation = Orientation(my_car.physics.rotation)
        car_direction = car_orientation.forward

        target = ball_location
        car_to_target = target - car_location
        steer_correction_radians = find_correction(car_direction, car_to_target)

        self.controller_state.throttle = 1.0
        self.controller_state.steer = -1 if steer_correction_radians > 0 else 1.0

        draw_debug(self.renderer, [goal_text, closest_text])

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


def draw_debug(renderer, text_lines: List[str]):
    renderer.begin_rendering()
    y = 250
    for line in text_lines:
        renderer.draw_string_2d(50, y, 1, 1, line, renderer.yellow())
        y += 20
    renderer.end_rendering()
