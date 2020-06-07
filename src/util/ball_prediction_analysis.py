from typing import Callable

from rlbot.utils.structures.ball_prediction_struct import BallPrediction, Slice

# field length(5120) + ball radius(93) = 5213 however that results in false positives
GOAL_THRESHOLD = 5235

# We will jump this number of frames when looking for a moment where the ball is inside the goal.
# Big number for efficiency, but not so big that the ball could go in and then back out during that
# time span. Unit is the number of frames in the ball prediction, and the prediction is at 60 frames per second.
COARSE_SEARCH_INCREMENT = 20


def find_slice_at_time(ball_prediction: BallPrediction, game_time: float):
    start_time = ball_prediction.slices[0].game_seconds
    approx_index = int((game_time - start_time) * 60)  # We know that there are 60 slices per second.
    if 0 <= approx_index < ball_prediction.num_slices:
        return ball_prediction.slices[approx_index]
    return None


def predict_future_goal(ball_prediction: BallPrediction):
    return find_matching_slice(ball_prediction, 0, lambda s: abs(s.physics.location.y) >= GOAL_THRESHOLD)


def find_matching_slice(ball_prediction: BallPrediction, start_index: int, predicate: Callable[[Slice], bool]):
    for coarse_index in range(start_index, ball_prediction.num_slices, COARSE_SEARCH_INCREMENT):
        if predicate(ball_prediction.slices[coarse_index]):
            for j in range(max(start_index, coarse_index - COARSE_SEARCH_INCREMENT), coarse_index):
                ball_slice = ball_prediction.slices[j]
                if predicate(ball_slice):
                    return ball_slice
    return None
