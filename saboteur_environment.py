from saboteur_base_environment import SaboteurBaseEnvironment

class SaboteurEnvironment(SaboteurBaseEnvironment):
    def __init__(self):
        super().__init__()

    def get_legal_actions(game_state):
        return []
    
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
    
    