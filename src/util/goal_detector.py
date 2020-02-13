from dataclasses import dataclass

from util.vec import Vec3

# field length(5120) + ball radius(93) = 5213 however that results in false positives
GOAL_THRESHOLD = 5235

# We will jump this number of frames when looking for a moment where the ball is inside the goal.
# Big number for efficiency, but not so big that the ball could go in and then back out during that
# time span. Unit is the number of frames in the ball prediction, and the prediction is at 60 frames per second.
COARSE_SEARCH_INCREMENT = 20


@dataclass
class FutureGoal:
    location: Vec3
    velocity: Vec3
    time: float


def find_future_goal(ball_predictions):
    for coarse_index in range(0, ball_predictions.num_slices, COARSE_SEARCH_INCREMENT):
        if abs(ball_predictions.slices[coarse_index].physics.location.y) >= GOAL_THRESHOLD:
            for j in range(max(0, coarse_index - COARSE_SEARCH_INCREMENT), coarse_index):
                slice = ball_predictions.slices[j]
                if abs(slice.physics.location.y) >= GOAL_THRESHOLD:
                    # returns the position the ball crosses the goal as well as the time it's predicted to occur
                    return FutureGoal(Vec3(slice.physics.location), Vec3(slice.physics.velocity), slice.game_seconds)
    return None
