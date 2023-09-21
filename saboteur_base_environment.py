import random
import numpy as np

from une_ai.models import GameEnvironment
from une_ai.models import GridMap

class InvalidMoveException(Exception):
    pass

class Saboteur_Base_Environment(GameEnvironment):

    N_COLS = 20
    N_ROWS = 20

    def __init__(self):
        super().__init__("Saboteur Game Environment")
        #Starting rules of the game

    def add_player(self, player):
        pass

    def get_game_state(self):
        pass

    def turn(): #Need to edit parameters
        pass

    def get_openings(): #Need to edit parameters
        pass

    def get_winner(): #Need to edit parameters
        pass

    def get_percepts(self):
        pass

    def is_valid_location(): #Need to edit parameters
        pass

    def is_board_full():
        pass

    def _change_player_turn(self):
        pass

    def _use_path_card():
        pass

    def _use_action_card():
        pass
    
    def transition_result():
        pass

    def state_transition(self, agent_actuators):
        pass

    