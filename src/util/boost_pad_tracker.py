from dataclasses import dataclass
from typing import List

from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket

from util.vec import Vec3


@dataclass
class BoostPad:
    location: Vec3
    is_full_boost: bool
    is_active: bool  # Active means it's available to be picked up
    timer: float  # Counts the number of seconds that the pad has been *inactive*


class BoostPadTracker:
    """
    This class merges together the boost pad location info with the is_active info so you can access it
    in one convenient list. For it to function correctly, you need to call initialize_boosts once when the
    game has started, and then update_boost_status every frame so that it knows which pads are active.
    """

    def __init__(self):
        self.boost_pads: List[BoostPad] = []
        self._full_boosts_only: List[BoostPad] = []

    def initialize_boosts(self, game_info: FieldInfoPacket):
        raw_boosts = [game_info.boost_pads[i] for i in range(game_info.num_boosts)]
        self.boost_pads: List[BoostPad] = [BoostPad(Vec3(rb.location), rb.is_full_boost, False, 0) for rb in raw_boosts]
        # Cache the list of full boosts since they're commonly requested.
        # They reference the same objects in the boost_pads list.
        self._full_boosts_only: List[BoostPad] = [bp for bp in self.boost_pads if bp.is_full_boost]

    def update_boost_status(self, packet: GameTickPacket):
        for i in range(packet.num_boost):
            our_pad = self.boost_pads[i]
            packet_pad = packet.game_boosts[i]
            our_pad.is_active = packet_pad.is_active
            our_pad.timer = packet_pad.timer

    def get_full_boosts(self) -> List[BoostPad]:
        return self._full_boosts_only
