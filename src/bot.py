import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3
from util.action_chain import Action_chain


class MyBot(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.ball_predictions = None
        self.current_action_chain = None
        self.time = 0
        self.delta_time = 0

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.delta_time = packet.game_info.seconds_elapsed-self.time
        self.time = packet.game_info.seconds_elapsed
        self.ball_predictions = self.get_ball_prediction_struct()
        predicted_goal = find_future_goal(self.ball_predictions)
        goal_text = "No Goal Threats"

        if predicted_goal:
            goal_text = f"Goal in {'%.4s' % str(predicted_goal[1]-packet.game_info.seconds_elapsed)}s"

        ball_location = Vec3(packet.game_ball.physics.location)

        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)

        car_to_ball = ball_location - car_location

        # Find the direction of our car using the Orientation class
        car_orientation = Orientation(my_car.physics.rotation)
        car_direction = car_orientation.forward

        steer_correction_radians = find_correction(car_direction, car_to_ball)

        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
            action_display = "turn left"
        else:
            turn = 1.0
            action_display = "turn right"

        self.controller_state.throttle = 1.0
        self.controller_state.steer = turn

        draw_debug(self.renderer, my_car, packet.game_ball, action_display,goal_text)

        if self.current_action_chain != None:
            if not self.current_action_chain.complete:
                self.controller_state = self.current_action_chain.update(self.delta_time)
            else:
                self.current_action_chain = None
        else:
            if int(self.time) % 5 == 0:
                self.current_action_chain = simple_front_flip_chain()

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



def draw_debug(renderer, car, ball, action_display,goal_text):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    renderer.draw_string_2d(100, 50, 3, 3, goal_text, renderer.yellow())
    renderer.end_rendering()

def find_future_goal(ball_predictions):
    for i in range(0, ball_predictions.num_slices):
        if abs(ball_predictions.slices[i].physics.location.y) >= 5235: #field length(5120) + ball radius(93) = 5213 however that results in false positives
            #returns the position the ball crosses the goal as well as the time it's predicted to occur
            return [Vec3(ball_predictions.slices[i].physics.location),ball_predictions.slices[i].game_seconds]

    return None

def simple_front_flip_chain():
    first_controller = SimpleControllerState()
    second_controller = SimpleControllerState()
    third_controller = SimpleControllerState()

    first_controller.jump = True
    first_duration = 0.1

    second_controller.jump = False
    second_controller.pitch = -1
    second_duration = 0.1

    third_controller.jump = True
    third_controller.pitch = -1
    third_duration = 0.1

    return Action_chain([first_controller,second_controller,third_controller],[first_duration,second_duration,
                                                                               third_duration])