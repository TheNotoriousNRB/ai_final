from une_ai.models import Agent
from une_ai.models import GridMap

class SaboteurPlayer(Agent):
    game_board = GridMap(20,20,None)

    def __init__(self, agent_name, agent_program):
        super().__init__(agent_name, agent_program)
    
    def is_valid_game_board(self, grid_map):
        if grid_map.get_width() != 20 or grid_map.get_height != 20:
            return False
        
        return True

    def add_all_sensors(self):
        self.add_sensor(
            'game-board-sensor',
            self.game_board,
            lambda v: isinstance(v, GridMap) and
            self.is_valid_game_board(v)
        )

        self.add_sensor(
            'turn-taking-indicator',
            '1',
            lambda v: isinstance(v, str) and v in {'1', '2', '3', '4', '5', '6', '7', '8'}
        )

        self.add_sensor(
            'hand-cards',
            [],
            lambda v: isinstance(v, list) and 
            len(v) == 4 and 
            all(isinstance(t, tuple) or isinstance(t, str) for t in v)
        )
    
    def add_all_actuators(self):
        self.add_actuator(
            'path-card-handler',
            ['cross-road',0,0],
            lambda v: isinstance(v, list) and 
            len(v) == 3 and
            v[0] in {'cross-road', 'vertical-tunnel', 'horizontal-tunnel', 'vertical-junction', 'horizontal-junction', 'turn', 'dead-end', 'reverse-turn'} and
            v[1] >= 0 and v[1] <= 19 and
            v[2] >=0 and v[2] <= 19
        )

        self.add_actuator(
            'map-card-handler',
            ['map', 14, 8],
            lambda v: isinstance(v, list) and
            len(v) == 3 and
            v[0] == 'map' and
            v[1] == 14 and
            v[2] in {8, 10, 12}
        )

        self.add_actuator(
            'dynamite-card-handler',
            ['dynamite', (0, 0)],
            lambda v: isinstance(v, list) and
            len(v) == 2 and
            v[0] == 'dynamite' and
            isinstance(v[1], tuple) and
            v[1] not in {(6,10), (14,8), (14,10), (14,12)} and
            all(isinstance(i, int) and i>=0 and i<=19 for i in v[1])
        )

        self.add_actuator(
            'sabotage-card-handler',
            ('sabotage', '1'),
            lambda v: isinstance(v, tuple) and
            len(v) == 2 and
            v[0] == 'sabotage' and
            isinstance(v[1], str) and 
            v[1] in {'1', '2', '3', '4', '5', '6', '7', '8'}
        )

        self.add_actuator(
            'mend-card-handler',
            ('mend', '1'),
            lambda v: isinstance(v, tuple) and
            len(v) == 2 and
            v[0] == 'sabotage' and
            isinstance(v[1], str) and 
            v[1] in {'1', '2', '3', '4', '5', '6', '7', '8'}
        )

        self.add_actuator(
            'turn-card-handler',
            False,
            lambda v: isinstance(v, bool)
        )

    
    def add_all_actions(self):
        path_cards = ['cross-road', 'vertical-tunnel', 'horizontal-tunnel', 'vertical-junction', 'horizontal-junction', 'turn', 'dead-end', 'reverse-turn']
        for i in range(len(path_cards)):
            for x in range(19):
                for y in range(19):

                    self.add_action(
                    'use-path-card-{}-{}-{}'.format(i, x, y),
                    lambda i=i, x=x, y=y: self.path_card_action(i, x, y)

                    self.add_action(
                    'turn-path-card-{}'.format(i, x, y),
                    lambda i=i: self.turn_path_card(i)
        )

            ) 
           

    def path_card_action(self, i, x, y):
        self._update_actuator_value('turn-card-handler', False)
        return {'path-card-handler': [i, x, y]}

    def turn_card_action(self, i, x, y):
        self._update_actuator_value('turn-card-handler', True)
        return {'path-card-handler': [i, x, y]}
