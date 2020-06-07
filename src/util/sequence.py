from dataclasses import dataclass
from typing import List

from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


@dataclass
class StepResult:
    controls: SimpleControllerState
    done: bool


class Step:
    def tick(self, packet: GameTickPacket) -> StepResult:
        raise NotImplementedError


class ControlStep(Step):
    def __init__(self, duration: float, controls: SimpleControllerState):
        self.duration = duration
        self.controls = controls
        self.start_time: float = None

    def tick(self, packet: GameTickPacket) -> StepResult:
        if self.start_time is None:
            self.start_time = packet.game_info.seconds_elapsed
        elapsed_time = packet.game_info.seconds_elapsed - self.start_time
        return StepResult(controls=self.controls, done=elapsed_time > self.duration)


class Sequence:
    def __init__(self, steps: List[Step]):
        self.steps = steps
        self.index = 0
        self.done = False

    def tick(self, packet: GameTickPacket):
        while True:
            if self.index >= len(self.steps):
                self.done = True
                return SimpleControllerState()
            step = self.steps[self.index]
            result = step.tick(packet)
            if result.done:
                self.index += 1
                if self.index >= len(self.steps):
                    self.done = True
            return result.controls
