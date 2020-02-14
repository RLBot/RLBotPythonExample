from RLUtilities.GameInfo import GameInfo
from RLUtilities.LinearAlgebra import vec3
from RLUtilities.Maneuvers import Aerial
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.drive import steer_toward_target
from util.sequence import Step, StepResult
from util.vec import Vec3


MAX_SPEED_WITHOUT_BOOST = 1410
SECONDS_PER_TICK = 0.008  # Assume a 120Hz game. It's OK if we're wrong, aerial will still go OK


class LineUpForAerialStep(Step):
    """
    This will cause the car to steer toward the target until it is lined up enough and going at
    an appropriate speed for a successful aerial.
    """
    def __init__(self, target: Vec3, arrival_time: float, index: int):
        self.target = target
        self.arrival_time = arrival_time
        self.index = index

    def tick(self, packet: GameTickPacket) -> StepResult:
        car = packet.game_cars[self.index]

        seconds_till_arrival = self.arrival_time - packet.game_info.seconds_elapsed
        if seconds_till_arrival <= 0:
            return StepResult(SimpleControllerState(), done=True)
        current_speed = Vec3(car.physics.velocity).length()
        avg_speed_needed = Vec3(car.physics.location).flat().dist(self.target.flat()) / seconds_till_arrival

        steering = steer_toward_target(car, self.target)
        controls = SimpleControllerState(
            steer=steering,
            throttle=1 if avg_speed_needed > current_speed else 0,
            boost=avg_speed_needed > current_speed and avg_speed_needed > MAX_SPEED_WITHOUT_BOOST)

        ready_to_jump = abs(steering) < 0.1 and current_speed / avg_speed_needed > 0.7

        return StepResult(controls, done=ready_to_jump)


class AerialStep(Step):
    """
    This uses the Aerial controller provided by RLUtilities. Thanks chip!
    It will take care of jumping off the ground and flying toward the target.
    This will only work properly if you call tick repeatedly on the same instance.
    """
    def __init__(self, target: Vec3, arrival_time: float, index: int):
        self.index = index
        self.aerial: Aerial = None
        self.game_info: GameInfo = None
        self.target = target
        self.arrival_time = arrival_time

    def tick(self, packet: GameTickPacket) -> StepResult:

        if self.game_info is None:
            self.game_info = GameInfo(self.index, packet.game_cars[self.index].team)
        self.game_info.read_packet(packet)

        if self.aerial is None:
            self.aerial = Aerial(self.game_info.my_car, vec3(self.target.x, self.target.y, self.target.z),
                                 self.arrival_time)

        self.aerial.step(SECONDS_PER_TICK)
        controls = SimpleControllerState()
        controls.boost = self.aerial.controls.boost
        controls.pitch = self.aerial.controls.pitch
        controls.yaw = self.aerial.controls.yaw
        controls.roll = self.aerial.controls.roll
        controls.jump = self.aerial.controls.jump

        return StepResult(controls, packet.game_info.seconds_elapsed > self.arrival_time)
