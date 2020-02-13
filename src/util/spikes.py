from rlbot.utils.structures.game_data_struct import PlayerInfo, GameTickPacket

from util.vec import Vec3


class SpikeWatcher:
    def __init__(self):
        self.carrying_car: PlayerInfo = None
        self.spike_moment = 0
        self.carry_duration = 0

    def read_packet(self, packet: GameTickPacket):
        ball_location = Vec3(packet.game_ball.physics.location)
        closest_candidate: PlayerInfo = None
        closest_distance = 999999
        for i in range(packet.num_cars):
            car = packet.game_cars[i]
            car_location = Vec3(car.physics.location)
            distance = car_location.dist(ball_location)
            if distance < 190:
                if distance < closest_distance:
                    closest_candidate = car
                    closest_distance = distance
        if closest_candidate != self.carrying_car and closest_candidate is not None:
            self.spike_moment = packet.game_info.seconds_elapsed

        self.carrying_car = closest_candidate
        if self.carrying_car is not None:
            self.carry_duration = packet.game_info.seconds_elapsed - self.spike_moment
            print(closest_distance)
