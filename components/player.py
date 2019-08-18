import pygame
import math
from components.weapon import Weapon
from components.bullet import Bullet
from components.entity import Entity

vec = pygame.math.Vector2

PLAYER = pygame.image.load('assets/ship.png')

class Player(Entity):
    """ represents the Player. """

    def __init__(self):
        super().__init__(PLAYER, (130, 200, 120))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 700 / 2 - 40
        self.rect.y = 330
        # self.rect.centerx = self.rect.width / 2
        self.speed = 4
        self.weapon = Weapon(Bullet)
        self.pos = (350, 350)
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
        angle%= 2*math.pi
        img = self.rot_center(self.image, math.degrees(angle))
        rect = img.get_rect()
        rect.center = self.rect.center
        screen.blit(img, rect)

    def move(self, direction):
        self.direction = direction

    def update(self, dt):
        """ update the player's position to the mouse x position """
        if self.direction == 'left':
            self.acc = vec(-700, 0)
        elif self.direction == 'right':
            self.acc = vec(700, 0)
        elif self.direction == 'stop':
            self.acc = vec(0 ,0)

        if self.pos[0] > 690:
            self.pos[0] = 690
        elif self.pos[0] < 10:
            self.pos[0] = 10
        super().update(dt)


        # if self.rect.centerx + 5 == 0 or self.rect.x - 5 == 0:
        #     self.rect.centerx = pos[0]
        # elif self.rect.centerx > pos[0] + 5:
        #     self.rect.x -= self.speed
        # elif self.rect.centerx < pos[0] - 5:
        #     self.rect.x += self.speed


