from saboteur_environment import SaboteurEnvironment
from saboteur_game import SaboteurGame
from saboteur_player import SaboteurPlayer
from agent_programs import random_behaviour

if __name__ == '__main__':

    playerOne = SaboteurPlayer('1', random_behaviour)
    playerTwo = SaboteurPlayer('2', random_behaviour)
    playerThree = SaboteurPlayer('3', random_behaviour)
    playerFour = SaboteurPlayer('4', random_behaviour)
    playerFive = SaboteurPlayer('5', random_behaviour)
    playerSix = SaboteurPlayer('6', random_behaviour)
    playerSeven = SaboteurPlayer('7', random_behaviour)
    playerEight = SaboteurPlayer('8', random_behaviour)

    game_environment = SaboteurEnvironment()


    game_environment.add_player(playerOne)
    game_environment.add_player(playerTwo)
    game_environment.add_player(playerThree)
    game_environment.add_player(playerFour)
    game_environment.add_player(playerFive)
    game_environment.add_player(playerSix)
    game_environment.add_player(playerSeven)
    game_environment.add_player(playerEight)

    game = SaboteurGame(playerOne, playerTwo, playerThree, playerFour, playerFive, playerSix, playerSeven, playerEight, game_environment)
