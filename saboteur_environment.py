from saboteur_base_environment import SaboteurBaseEnvironment
from card import PathCard, ActionCard


class SaboteurEnvironment(SaboteurBaseEnvironment):
    def __init__(self):
        super().__init__()

    def get_legal_actions(game_state):
        legal_actions = []
        game_board = game_state['game-board']
        player_turn = SaboteurBaseEnvironment.turn(game_state)
        player_card = SaboteurBaseEnvironment.get_hand_cards()

        for x in range(20):
            for y in range(20):
                if SaboteurBaseEnvironment.is_empty(x, y) and SaboteurBaseEnvironment.is_adjacent_to_tunnel(x, y):
                    for card in player_card:
                        if isinstance(card, PathCard):
                            legal_actions.append(f'use-path-card-{card}-{x}-{y}')

        return legal_actions
    
    def get_winner(game_state):
        game_board = game_state['game-board']
        if SaboteurBaseEnvironment._all_cards_played() == True or len(SaboteurEnvironment.get_legal_actions() == 0):
            return "Saboteur"
        if SaboteurBaseEnvironment._path_connected() == True:
            return "Gold-Diggers"
        return None
    
    def is_terminal(game_state):
        if SaboteurEnvironment.get_winner(game_state) is not None:
            return True
    
    