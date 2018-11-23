from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from RLUtilities.GameInfo import GameInfo
from .base_mechanic import BaseMechanic


class BaseTestAgent(BaseAgent):

    def __init__(self, name, team, index):
        super(BaseTestAgent, self).__init__(name, team, index)
        self.info = GameInfo(index, team)

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        self.info.read_packet(game_tick_packet)
        self.test_process(game_tick_packet)
        return self.get_mechanic_controls()

    def get_mechanic_controls(self) -> BaseMechanic:
        raise NotImplementedError

    def test_process(self, game_tick_packet: GameTickPacket):
        raise NotImplementedError

    def initialize_agent(self):
        raise NotImplementedError
