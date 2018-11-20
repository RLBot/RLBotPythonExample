from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from RLUtilities.GameInfo import GameInfo
from .base_action import BaseAction


class BaseTestAgent(BaseAgent):
    def __init__(self, name, team, index):
        super(BaseTestAgent, self).__init__(name, team, index)
        self.action = self.create_action()
        self.info = GameInfo(index, team)

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        self.info.read_packet(game_tick_packet)
        self.test_process(game_tick_packet)
        return self.action.get_output(self.info)

    def create_action(self) -> BaseAction:
        raise NotImplementedError

    def test_process(self, game_tick_packet: GameTickPacket):
        raise NotImplementedError

    def initialize_agent(self):
        raise NotImplementedError
