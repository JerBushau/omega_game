import pygame
import math
from components.weapon import Weapon
from components.bullet import Bullet
from components.entity import Entity

HEIGHT = 400
WIDTH = 700

vec = pygame.math.Vector2

PLAYER = pygame.image.load('assets/ship.png')

class Player(Entity):
    """ represents the Player. """

    def __init__(self):
        super().__init__(PLAYER, (200, 800, 120))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.weapon = Weapon(Bullet)
        self.pos = (WIDTH / 2, HEIGHT - 40)
        self.direction = 'stop'

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self, screen):
        """ draw player specifically """
        mouse_pos = pygame.mouse.get_pos()
        des = self.pos - vec(mouse_pos)
        angle = math.atan2(des.x, des.y)
        angle%=2*math.pi
        img = self.rot_center(self.image, math.degrees(angle))
        rect = img.get_rect()
        rect.center = self.rect.center

        # rect.clamp_ip(screen.get_rect())
        screen.blit(img, rect)

    def move(self, direction):
        self.direction = direction

    def update(self, dt):
        """ update the player's position to the mouse x position """

        if self.direction == 'left':
            self.acc = vec(-1, 0).normalize() * self.max_speed
        elif self.direction == 'right':
            self.acc = vec(701, 0).normalize() * self.max_speed
        elif self.direction == 'stop':
            self.acc = vec(0 ,0)

        # give edges of screen a little bounce when hit
        if self.pos[0] >= (WIDTH -30):
            self.pos[0] = WIDTH -30
            self.acc = vec(-1, 0).normalize() * 2000
        elif self.pos[0] <= 30:
            self.pos[0] = 30
            self.acc = vec(701, 0).normalize() * 2000

        super().update(dt)


