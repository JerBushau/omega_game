import pygame
import random
import time
from components.background import Background
from components.hud import Hud
from levels.level1 import Level1
from score import scores
from timer import Timer2
from gamestate import GameState
from game import Game


START_BG = 'assets/start_bg.png'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# handy functions from a tutorial needs re-write to better suit my needs
def text_objects(text, font, color):
    """Creates 'text objects' for displaying messages"""
    text_surf = font.render(text, True, color)
    return text_surf, text_surf.get_rect()


# create a button class rather than this function
def button(msg, x, y, width, height, colors, surface, action=None):
    """Function to easily create buttons"""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, colors[0], (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(surface, colors[1], (x, y, width, height))

    small_text = pygame.font.Font('freesansbold.ttf',20)
    text_surf, text_rect = text_objects(msg, small_text, colors[2])
    text_rect.center = ((x + (width/2)),(y + (height / 2)))
    surface.blit(text_surf, text_rect)
    pygame.display.update()


class StartScreen(GameState):

    def __init__(self):
        super().__init__()
        self.background = Background(START_BG, [0, 0])
        self.top_score_hud = Hud(10, 350, 200, 40, "TOP SCORE")
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

        large_text = pygame.font.Font('freesansbold.ttf',80)
        text_surf, text_rect = text_objects("OMEGA!", large_text, (210,208,224))
        text_rect.center = ((700/2),(400/2.75))
        surface.blit(text_surf, text_rect)
        button('PLAY', ((700/2) - 50), 240, 100, 40,
              ((37,31,71), (108,100,153), (210,208,224)), surface, self.end)

    def update(self, dt):
        self.top_score_hud.prop = self.scores.top_score


if __name__ == '__main__':
    pygame.mixer.pre_init(frequency=22050, size=8, channels=2, buffer=1024)
    pygame.init()
    screen = pygame.display.set_mode((700, 400))
    states = {"START": StartScreen(),
              "LEVEL1": Level1()}
    game = Game(screen, states, "START")
    game.run()


    pygame.quit()
    quit()
