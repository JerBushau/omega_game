import pygame
import time
from components.background import Background
from components.hud import Hud
from components.button import Button
from levels.level1 import Level1
from score import scores
from gamestate import GameState
from game import Game
from helpers import text_objects, button


START_BG = 'assets/background_start.png'
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
        self.button_list = pygame.sprite.Group()

        start_button = Button((WIDTH/2-50), HEIGHT/1.75,
                100, 40, self.end, text="PLAY", font=pygame.font.Font('freesansbold.ttf', 20)).add(self.button_list)

        super().startup(persistent)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        for btn in self.button_list:
            btn.handle_event(event)

    def end(self):
        self.done = True

    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.background.image, self.background.rect)
        self.top_score_hud.update(dest=surface)
        self.button_list.draw(surface)

        large_text = pygame.font.Font('./assets/fonts/Sansation-Bold.ttf', 120)
        text_surf, text_rect = text_objects("OMEGA!", large_text, (210,208,224))
        text_rect.center = ((WIDTH/2),(HEIGHT/2.55))
        surface.blit(text_surf, text_rect)

    def update(self, dt):
        self.top_score_hud.prop = self.scores.top_score
        self.button_list.update()


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
