import random
import numpy as np

from une_ai.models import GameEnvironment
from une_ai.models import GridMap
from card import PathCard, ActionCard
from deck import Deck
from game_board import GameBoard

class InvalidMoveException(Exception):
    pass

class SaboteurBaseEnvironment(GameEnvironment):

    ROLES = ['Gold-Digger', 'Saboteur']

    def __init__(self):
        super().__init__("Saboteur Game Environment")
        self._game_board = GameBoard.get_board()
        self._played_cards = None
        self._roles = ['Gold-Digger'] * 6 + ['Saboteur'] * 3
        self._player_turn = random.choices(self._players.keys())
        self._card_deck = Deck()._deck
        self._total_cards = len(self._card_deck)

    
    def add_player(self, player):
        assert len(self._players) < 8, "It is not possible to add more than 8 players, in the game"

        _player_cards = self.initialize_player_cards() #getting starting cards for each player
        self._players[player] = (self._roles.pop(random.choice(self._roles)), _player_cards) #adding player with playerId, playerRole and starting cards
        return player
    
    def get_hand_cards(self):
        return (self._players.get(self._player_turn))[1]
    
    def get_game_state(self):
        game_state = {
            'game-board': self._game_board.copy(),
            'player-turn': self._player_turn,
            'player-hand-card': self.get_hand_cards(),
            'card-deck': self._card_deck
        }
        return game_state

    def initialize_player_cards(self):
        player_cards = ['']
        for i in range(4):
            player_cards.append(self._card_deck.draw())

        return player_cards
    
    def turn(game_state):
        return game_state['player-turn']
    
    def _change_player_turn(self):
        self._prev_turn = self._player_turn
        next_turn = int(self._prev_turn) + 1
        if next_turn == 9:
            self._player_turn = '1'
        else: 
            self._player_turn = str(next_turn)
    
    def get_percepts(self):
        game_state = self.get_game_state()
        return {
            'game-board-sensor': game_state['game-board'],
            'turn-taking-indicator': self._player_turn,
            'hand-cards': self.get_hand_cards()
        }
    
    def transition_result(game_state, action):
        pass

    def _all_cards_played(self):
        return len(self._card_deck) == 0 and all(len(player[1]) == 0 for player in self._players.values())
    
    def _path_connected(self):
        return False
        
