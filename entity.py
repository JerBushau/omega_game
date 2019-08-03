import pygame
from random import randint, uniform

vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400
# Boss properties
BOSS_SIZE = 32
MAX_SPEED = 2
MAX_FORCE = 0.03
APPROACH_RADIUS = 120

class Entity(pygame.sprite.Sprite):
    """The base class for any on screen object with movement"""

    def __init__(self, img, starting_pos=(100, 100)):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.pos = vec(starting_pos)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos


    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer


    def update(self):
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos
