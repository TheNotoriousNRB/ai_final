import traceback
import random
import time
import math

from une_ai.models import GraphNode

from saboteur_game import SaboteurGame
from saboteur_base_environment import SaboteurBaseEnvironment as base
from saboteur_environment import SaboteurEnvironment as gm

def random_behaviour(percepts, actuators):
    try:
        game_state = {
            'game-board': percepts['game-board-sensor'],
            'player-turn': percepts['turn-taking-indicator'],
            'player-hand-card': percepts['hand-cards-sensor'],
        }
    except KeyError as e:
        game_state = {}
        print("You may have forgotton to add the necessary sensor")
        traceback.print_exc()

    if not gm.is_terminal(game_state):
        legal_moves = gm.get_legal_actions(game_state)
        try:
            print(legal_moves)
            action = random.choice(legal_moves)
        except IndexError as e:
            print("You may have forgotten to implement the ConnectFourEnvironment methods, or you implemented them incorrectly:")
            traceback.print_exc()
            return []
        
        return [action]
    else:
        return []