from util.mechanic.base_mechanic import BaseMechanic
from rlbot.agents.base_agent import SimpleControllerState
from RLUtilities.Simulation import Car
from RLUtilities.LinearAlgebra import vec3, dot, transpose, rotation_to_axis, norm
from RLUtilities.Maneuvers import look_at, AerialTurn
from .PD import *


class BaseFaceVector(BaseMechanic):

    def step(self, car: Car, target: vec3) -> SimpleControllerState:
        self.car = car
        self.target = target

        local_pos = dot(self.target, self.car.theta)
        local_pos_spherical = spherical(local_pos)
        local_omega = dot(self.car.omega, self.car.theta)

        theta_error = math.sqrt(local_pos_spherical[1]**2 + local_pos_spherical[2]**2)
        omega_error = math.sqrt(local_omega[1]**2 + local_omega[2]**2)

        if omega_error < 0.1 and theta_error < 0.1:
            self.finished = True
        else:
            self.finished = False


class FaceVectorRLU(BaseFaceVector):

    def step(self, car: Car, target: vec3, dt: float = 0.01667) -> SimpleControllerState:
        super(FaceVectorRLU, self).step(car, target)

        target_rotation = look_at(self.target)
        self.action = AerialTurn(car, target_rotation)

        self.action.step(dt)
        self.controls = self.action.controls

        self.car.last_input.pitch = self.controls.pitch
        self.car.last_input.yaw = self.controls.yaw
        self.car.last_input.roll = self.controls.roll

        return self.controls


class FaceVectorPD(BaseFaceVector):

    def step(self, car: Car, target: vec3) -> SimpleControllerState:
        super(FaceVectorPD, self).step(car, target)

        local_pos = dot(self.target, self.car.theta)
        local_pos_spherical = spherical(local_pos)
        roll = rotationMatrixToEulerAngles(self.car.theta)[0]

        local_omega = dot(self.car.omega, self.car.theta)

        self.controls.pitch = pitch_point(local_pos_spherical[1], local_omega[1])
        self.controls.yaw = yaw_point(local_pos_spherical[2], local_omega[2])
        self.controls.roll = roll_point(roll, local_omega[0])

        return self.controls
