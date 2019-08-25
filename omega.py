import pygame
import time
from components.background import Background
from components.hud import Hud
from levels.level1 import Level1
from score import scores
from gamestate import GameState
from game import Game
from helpers import text_objects, button


START_BG = 'assets/start_bg.png'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH = 1050
HEIGHT = 600

class StartScreen(GameState):

    def __init__(self):
        super().__init__()
        self.background = Background(START_BG, [0, 0])
        self.top_score_hud = Hud(10, HEIGHT-50, 200, 40, "TOP SCORE")
        self.scores = scores
        self.next_state = 'LEVEL1'

    def startup(self, persistent):
        pygame.mouse.set_visible(True)
        super().startup(persistent)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def end(self):
        self.done = True

    def draw(self, surface):
        surface.blit(self.background.image, self.background.rect)
        self.top_score_hud.update(dest=surface)

        large_text = pygame.font.Font('freesansbold.ttf', 120)
        text_surf, text_rect = text_objects("OMEGA!", large_text, (210,208,224))
        text_rect.center = ((WIDTH/2),(HEIGHT/2.55))
        surface.blit(text_surf, text_rect)
        button('PLAY', ((WIDTH/2) - 50), HEIGHT/1.95, 100, 40,
              ((37,31,71), (108,100,153), (210,208,224)), surface, self.end)

    def update(self, dt):
        self.top_score_hud.prop = self.scores.top_score


if __name__ == '__main__':
    pygame.mixer.pre_init(frequency=22050, size=8, channels=2, buffer=1024)
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    states = {"START": StartScreen(),
              "LEVEL1": Level1()}
    game = Game(screen, states, "START")
    game.run()


    pygame.quit()
    quit()
