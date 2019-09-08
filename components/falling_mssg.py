import pygame
from components.mssg import Mssg
from timer import Timer

WIDTH = 1050
HEIGHT = 600

vec = pygame.math.Vector2

class FallingMssg(Mssg):
    def __init__(self, text, color, callback, pos=((WIDTH/2), 0), font_size=17, *groups):
        super().__init__(text, color, pos, font_size, groups)
        self.cb_timer = Timer(1000)
        self.cb = callback
        self.dies_off_screen = False
        self.max_speed = 180


    def update(self, dt):
        super().update(dt)

        self.acc = vec(0, 1) * self.max_speed

        if self.rect.y >= HEIGHT and not self.cb_timer.is_active:
            self.cb_timer.start();

        if self.cb_timer.is_finished():
            self.cb()
            # self.kill()