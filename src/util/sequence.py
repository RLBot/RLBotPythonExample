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
        """
        Return appropriate controls for this step in the sequence. If the step is over, you should
        set done to True in the result, and we'll move on to the next step during the next frame.
        If you panic and can't return controls at all, you may return None and we will move on to
        the next step immediately.
        """
        raise NotImplementedError


class ControlStep(Step):
    """
    This allows you to repeat the same controls every frame for some specified duration. It's useful for
    scheduling the button presses needed for kickoffs / dodges / etc.
    """
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
        while self.index < len(self.steps):
            step = self.steps[self.index]
            result = step.tick(packet)
            if result is None or result.controls is None or result.done:
                self.index += 1
                if self.index >= len(self.steps):
                    # The bot will know not to use this sequence next frame, even though we may be giving it controls.
                    self.done = True
            if result is not None and result.controls is not None:
                # If the step was able to give us controls, return them to the bot.
                return result.controls
            # Otherwise we will loop to the next step in the sequence.
        # If we reach here, we ran out of steps to attempt.
        self.done = True
        return None
