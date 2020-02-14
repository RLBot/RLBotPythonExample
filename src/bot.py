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

# Would you like to use numpy utilities? Check out the np_util folder!

class MyBot(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.active_sequence: Sequence = None
        self.spike_watcher = SpikeWatcher()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """

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
        if 550 < car_velocity.length < 600:
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

        # The rest of this code just ball chases.
        # Find the direction of your car using the Orientation class
        car_orientation = Orientation(my_car.physics.rotation)
        car_direction = car_orientation.forward

        target = ball_location
        car_to_target = target - car_location
        steer_correction_radians = find_correction(car_direction, car_to_target)

        self.controller_state.throttle = 1.0

        # Change the multiplier to influence the sharpness of steering. You'll wiggle if it's too high.
        self.controller_state.steer = limit_to_safe_range(-steer_correction_radians * 5)

        draw_debug(self.renderer, [goal_text])

        return self.controller_state


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


def find_correction(current: Vec3, ideal: Vec3) -> float:
    """
    Finds the angle from current to ideal vector in the xy-plane. Angle will be between -pi and +pi.
    """

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
    """
    This will draw the lines of text in the upper left corner.
    This function will automatically put appropriate spacing between each line
    so they don't overlap.
    """
    renderer.begin_rendering()
    y = 250
    for line in text_lines:
        renderer.draw_string_2d(50, y, 1, 1, line, renderer.yellow())
        y += 20
    renderer.end_rendering()
