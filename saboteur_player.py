from une_ai.models import Agent
from une_ai.models import GridMap
from card import PathCard
from card import ActionCard

class SaboteurPlayer(Agent):
    game_board = GridMap(20,20,None)
    path_cards = [PathCard.cross_road, PathCard.vertical_tunnel, PathCard.horizontal_tunnel, PathCard.vertical_junction, PathCard.horizontal_junction, PathCard.turn, PathCard.dead_end, PathCard.reversed_turn]
    map_cards = [(14,8), (14,10), (14,12)]
    special_cards = [(14,8), (14,10), (14,12), (6,10)]

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
            (PathCard.cross_road,(0,0)),
            lambda v: isinstance(v, tuple) and 
            len(v) == 2 and
            isinstance(v[0], str) and
            v[0] in self.path_cards and
            isinstance(v[1], tuple) and
            len(v[1] == 2) and
            v[1][0] >= 0 and v[1][0] <= 19 and
            v[1][1] >=0 and v[1][1] <= 19
        )

        self.add_actuator(
            'map-card-handler',
            (ActionCard('map'),(0,0)),
            lambda v: isinstance(v, tuple) and 
            len(v) == 2 and
            isinstance(v[0], str) and
            isinstance(v[0], ActionCard) and v[0].get_action() == 'map' and
            isinstance(v[1], tuple) and
            len(v[1] == 2) and
            v[1][0] >= 0 and v[1][0] <= 19 and
            v[1][1] >=0 and v[1][1] <= 19 and
            v[1] in self.map_cards
        )

        self.add_actuator(
            'dynamite-card-handler',
            (ActionCard('dynamite'), (0, 0)),
            lambda v: isinstance(v, list) and
            len(v) == 2 and
            isinstance(v[0], ActionCard) and v[0].get_action() == 'dynamite' and 
            isinstance(v[1], tuple) and
            len(v[1] == 2) and
            v[1][0] >= 0 and v[1][0] <= 19 and
            v[1][1] >=0 and v[1][1] <= 19 and
            v[1] not in self.special_cards
        )

        self.add_actuator(
            'sabotage-card-handler',
            (ActionCard('sabotage'), '1'),
            lambda v: isinstance(v, tuple) and
            len(v) == 2 and
            isinstance(v[0], ActionCard) and v[0].get_action() == 'sabotage' and
            isinstance(v[1], str) and 
            v[1] in {'1', '2', '3', '4', '5', '6', '7', '8'}
        )

        self.add_actuator(
            'mend-card-handler',
            (ActionCard('mend'), '1'),
            lambda v: isinstance(v, tuple) and
            len(v) == 2 and
            isinstance(v[0], ActionCard) and v[0].get_action() == 'mend' and
            isinstance(v[1], str) and 
            v[1] in {'1', '2', '3', '4', '5', '6', '7', '8'}
        )

        self.add_actuator(
            'turn-card-handler',
            False,
            lambda v: isinstance(v, bool)
         )

    
    def add_all_actions(self):
       
        for i in range(len(self.path_cards)):
            for x in range(20):
                for y in range(20):
                    self.add_action(
                    'use-path-card-{}-{}-{}'.format(i, x, y),
                    lambda i=i, x=x, y=y: {self.path_card_action(i, x, y)} if not (x, y) in self.special_cards else {}
                    )

                    self.add_action(
                    'turn-path-card-{}-{}-{}'.format(i, x, y),
                    lambda i=i, x=x, y=y: {self.turn_path_card(i, x, y)} if not (x, y) in self.special_cards else {}
                    )



        for i in range(len(self.map_cards)):
            self.add_action(
                'use-map-card-{}-{}'.format(self.map_cards[i][0], self.map_cards[i][1]),
                lambda i=i, map_cards=self.map_cards: {'map-card-handler': (ActionCard('map'), (map_cards[i][0], map_cards[i][1]))}
            )
        
        for x in range(20):
            for y in range(20):
                self.add_action(
                    'dynamite-card-{}-{}'.format(x, y),
                    lambda x=x, y=y: {'dynamite-card-handler': (ActionCard('dynamite'), (x, y))} if not (x, y) in self.special_cards else {}
                    )
        
        for i in range(8):
            self.add_action(
                'sabotage-card-{}'.format(i+1),
                lambda: {'sabotage-card-handler': (ActionCard('sabotage'), i+1)}
            )
        
        for i in range(8):
            self.add_action(
                'mend-card-{}'.format(i+1),
                lambda: {'mend-card-handler': (ActionCard('mend'), i+1)}
            )

    def path_card_action(self, path_card, x, y):
        self._update_actuator_value('turn-card-handler', False)
        return {'path-card-handler': (path_card, (x,y))}

    def turn_card_action(self, path_card, x, y):
        self._update_actuator_value('turn-card-handler', True)
        return {'path-card-handler': (PathCard.turn_card(path_card), (x,y))}
