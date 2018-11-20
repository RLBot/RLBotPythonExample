from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from RLUtilities.GameInfo import GameInfo


class BaseAction:
    def get_output(self, info: GameInfo) -> SimpleControllerState:
        raise NotImplementedError
