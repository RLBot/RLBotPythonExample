from rlbot.utils.structures.game_data_struct import PlayerInfo, GameTickPacket

from util.vec import Vec3

# When the ball is attached to a car's spikes, the distance will vary a bit depending on whether the ball is
# on the front bumper, the roof, etc. It tends to be most far away when the ball is on one of the front corners
# and that distance is a little under 200. We want to be sure that it's never over 200, otherwise bots will
# suffer from bad bugs when they don't think the ball is spiked to them but it actually is; they'll probably
# drive in circles. The opposite problem, where they think it's spiked before it really is, is not so bad because
# they usually spike it for real a split second later.
MAX_DISTANCE_WHEN_SPIKED = 200

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
            if distance < MAX_DISTANCE_WHEN_SPIKED:
                if distance < closest_distance:
                    closest_candidate = car
                    closest_distance = distance
        if closest_candidate != self.carrying_car and closest_candidate is not None:
            self.spike_moment = packet.game_info.seconds_elapsed

        self.carrying_car = closest_candidate
        if self.carrying_car is not None:
            self.carry_duration = packet.game_info.seconds_elapsed - self.spike_moment
