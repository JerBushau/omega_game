import pygame
import random
from components.entity import Entity

vec = pygame.math.Vector2

WOBBLE = pygame.image.load('assets/wobble.png')
WIDTH = 1050
HEIGHT = 600

class Chain_Lightning(Entity):
    """Bullet type class that will jump from enemy to enemy"""

    def __init__(self, pos, *groups):
        super().__init__(WOBBLE, (580, 1500, 120), pos, groups)
        self.next_target = None
        self.enemy_list = None

    def find_next_target(self, enemy_list):
        """Find next available target"""
        if self.enemy_list == None:
            self.enemy_list = enemy_list
        if len(enemy_list) > 0:
            enemy = enemy_list[random.randint(0, len(enemy_list) - 1)]
            if not enemy.hit and enemy.alive:
                self.next_target = enemy


    def update(self, dt):
        """ update movement and state """
        m_pos = pygame.mouse.get_pos()

        if self.next_target != None:
            self.acc = self.seek(self.next_target.pos)

            if self.next_target.hit:
                self.find_next_target(self.enemy_list)
                if len(self.next_target.groups()) == 0:
                    self.acc = self.seek(m_pos)
                else:
                    self.acc = self.seek(self.next_target.pos)
        else:
            self.find_next_target(self.enemy_list)
            if self.next_target != None:
                self.acc = self.seek(self.next_target.pos)
            else:
                self.acc = self.seek(m_pos)

        super().update(dt)
