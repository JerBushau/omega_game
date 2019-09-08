import pygame
from random import randint
from components.mssg import Mssg

WIDTH = 1050
HEIGHT = 600

vec = pygame.math.Vector2

class OnScreenDmg(Mssg):
    def __init__(self, text, color, pos=((WIDTH/2), 0), font_size=17, *groups):
        super().__init__(text, color, pos, font_size, groups)
        self.falling = False
        self.random_x = randint(-55, 55)

    def update(self, dt):
        if self.pos[1] < self.starting_pos[1] - 20: 
            self.falling = True

        if not self.falling:
            self.acc = vec(self.random_x, -100) * 5
        else:
            self.acc = vec(self.random_x, 600)

        super().update(dt)