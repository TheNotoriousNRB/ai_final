import pygame
import numpy as np
import os
from card import PathCard

BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (125, 125, 125)
BLUE = (10, 20, 200)
GREEN = (255, 125, 125)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
#POWERUPS_BAR_HEIGHT = 35
#SCORE_BAR_HEIGHT = 35
INFO_BAR_HEIGHT = 35
BOX_SIZE = 40

class SaboteurGame:
    def __init__(self, player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8, environment, is_debugging=False, display_w=DISPLAY_WIDTH, display_h=DISPLAY_HEIGHT):
        pygame.init()
        window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT+INFO_BAR_HEIGHT))
        pygame.display.set_caption('Saboteur')
        window_clock = pygame.time.Clock()

        self._card_image = pygame.image.load(os.path.join('images/', 'cross-road.png'))
        self._scaled_card_image = pygame.transform.scale(self._card_image, (40, 40))
        self._start_card = PathCard.cross_road(special_card='start')



        self._display = window
        self._window_clock = window_clock
        self._display_size = (display_w, display_h)
        self._players = {}
        self._players['1'] = player_1
        self._players['2'] = player_2
        self._players['3'] = player_3
        self._players['4'] = player_4
        self._players['5'] = player_5
        self._players['6'] = player_6
        self._players['7'] = player_7
        self._players['8'] = player_8
        self._environment = environment
        self._last_action = ""
        self._is_debugging = is_debugging
        self._box_size = BOX_SIZE

        game_state = self._environment.get_game_state()
        game_board = game_state['game-board']
        self._n_cols = game_board.get_width()
        self._n_rows = game_board.get_height()

        self._coordinates = np.array([[None]*self._n_cols]*self._n_rows)
        for y in range(self._n_rows):
            for x in range(self._n_cols):
                self._coordinates[y, x] = (x, y)

        fonts = pygame.font.get_fonts()
        self._font = fonts[0] # default to a random font
        # try to look among the most common fonts
        test_fonts = ['arial', 'couriernew', 'verdana', 'helvetica', 'roboto']
        for font in test_fonts:
            if font in fonts:
                self._font = font
                break

        self.main()

    def _draw_text(self, text_message, font_size = 20):
        font = pygame.font.SysFont(self._font, font_size)
        text_size = font.size(text_message)
        text = font.render(text_message, True, WHITE)

        self._display.blit(text, (DISPLAY_WIDTH/2 - len(text_message), 20))
    
    def _draw_box(self, x, y, card):
        card_color = WHITE 
        x_coord = x * self._box_size
        y_coord = y * self._box_size
        image = None
        if card.is_cross_road():
            image = self._scaled_card_image
            self._display.blit(image, (x_coord, y_coord))
        else:
            pygame.draw.rect(self._display, card_color, pygame.Rect(x_coord, y_coord, self._box_size, self._box_size))


    def _draw_board(self):
        game_state = self._environment.get_game_state()
        game_board = game_state['game-board']
        for y in range(self._n_rows):
            for x in range(self._n_cols):
                card = game_board.get_item_value(x, y)
                if card:
                    self._environment.get_legal_actions()
                    self._draw_box(x, y, card)

    
    def _reset_bg(self):
        self._display.fill(BLACK)
    
    def _draw_frame(self):
        self._reset_bg()
        self._draw_text("Start Game! this is you time", 15)
        self._draw_board()

    
    def main(self):
        running = True
        while running:
            self._draw_frame()
            pygame.display.update()
            self._window_clock.tick(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    quit()

            #self._play_step()
            if self._is_debugging:
                pygame.time.delay(2000)