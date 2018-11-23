from util.mechanic.base_mechanic import BaseMechanic
from rlbot.agents.base_agent import SimpleControllerState
from RLUtilities.Simulation import Car
from RLUtilities.LinearAlgebra import vec3
from RLUtilities.Maneuvers import look_at, AerialTurn


class FaceVector(BaseMechanic):

    def __init__(self, car: Car, target: vec3):
        super(FaceVector, self).__init__()
        self.car = car
        self.target = target

    def step(self, dt: float) -> SimpleControllerState:

        up = vec3(0, 0, 1)
        # up = vec3(*[self.car.theta[i, 2] for i in range(3)])

        target_rotation = look_at(self.target, up)
        self.action = AerialTurn(self.car, target_rotation)

        self.action.step(dt)
        self.controls = self.action.controls

        self.car.last_input.pitch = self.controls.pitch
        self.car.last_input.yaw = self.controls.yaw
        self.car.last_input.roll = self.controls.roll

        return self.controls
