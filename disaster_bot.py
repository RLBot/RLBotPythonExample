from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


class DisasterBot(BaseAgent):

    def initialize_agent(self):
        self.controls = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        return self.controls
