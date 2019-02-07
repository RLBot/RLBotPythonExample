from dataclasses import dataclass, field
from math import sqrt
from typing import Optional

from rlbot.training.training import Grade, Pass, Fail

from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.common_graders.timeout import FailOnTimeout
from rlbottraining.common_graders.compound_grader import CompoundGrader
from rlbottraining.grading.grader import Grader

class DriveToBallGrader(CompoundGrader):
    def __init__(self, timeout_seconds=4.0, min_dist_to_pass=200):
        super().__init__([
            PassOnNearBall(min_dist_to_pass=min_dist_to_pass),
            FailOnTimeout(timeout_seconds),
        ])

@dataclass
class PassOnNearBall(Grader):
    min_dist_to_pass: float = 200
    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        car = tick.game_tick_packet.game_cars[0].physics.location
        ball = tick.game_tick_packet.game_ball.physics.location

        dist = sqrt(
            (car.x - ball.x) ** 2 +
            (car.y - ball.y) ** 2
        )
        if dist <= self.min_dist_to_pass:
            return Pass()
        return None
