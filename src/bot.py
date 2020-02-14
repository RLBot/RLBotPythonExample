from typing import List

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.quick_chats import QuickChats

from util.aerial import AerialStep, LineUpForAerialStep
from util.drive import steer_toward_target
from util.goal_detector import find_future_goal
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

        # This is good to keep at the beginning of get_output. It will allow you to continue
        # any sequences that you may have started during a previous call to get_output.
        if self.active_sequence and not self.active_sequence.done:
            return self.active_sequence.tick(packet)

        self.spike_watcher.read_packet(packet)
        ball_prediction = self.get_ball_prediction_struct()

        # Example of predicting a goal event
        predicted_goal = find_future_goal(ball_prediction)
        goal_text = "No Goal Threats"
        if predicted_goal:
            goal_text = f"Goal in {predicted_goal.time - packet.game_info.seconds_elapsed:.2f}s"

        my_car = packet.game_cars[self.index]
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
        # then release it 2 seconds later.
        if self.spike_watcher.carrying_car == my_car:
            if self.spike_watcher.carry_duration == 0:
                self.send_quick_chat(QuickChats.CHAT_EVERYONE, QuickChats.Information_IGotIt)
            elif self.spike_watcher.carry_duration > 2:
                return SimpleControllerState(use_item=True)

        # Example of doing an aerial. This will cause the car to jump and fly toward the
        # ceiling in the middle of the field.
        if my_car.boost > 50 and my_car.has_wheel_contact:
            self.start_aerial(Vec3(0, 0, 2000), packet.game_info.seconds_elapsed + 4)

        # If nothing else interesting happened, just chase the ball!
        ball_location = Vec3(packet.game_ball.physics.location)
        self.controller_state.steer = steer_toward_target(my_car, ball_location)
        self.controller_state.throttle = 1.0

        # Draw some text on the screen
        draw_debug(self.renderer, [goal_text])

        return self.controller_state

    def start_aerial(self, target: Vec3, arrival_time: float):
        self.active_sequence = Sequence([
            LineUpForAerialStep(target, arrival_time, self.index),
            AerialStep(target, arrival_time, self.index)])


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
