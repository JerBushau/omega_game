import pygame
from random import randint, uniform
from entity import Entity
from timer import Timer
vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400

ENEMY = pygame.image.load('assets/enemy.png')
DESTRO_ENEMY = pygame.image.load('assets/destro_enemy.png')

class Boss(Entity):
    """Boss entity"""

    def __init__(self):
        super().__init__(pygame.transform.scale(ENEMY.convert_alpha(), (60, 60)))
        self.hp = 100
        self.attack_timer = Timer()
        self.is_in_attack_mode = False
        self.attack_duration = randint(180, 360)


    def draw(self, screen):
        """ draw boss specifically """
        screen.blit(self.image, self.rect)


    def update(self, target):

        self.attack_timer.start_timer()
    
        if self.is_in_attack_mode == True:
            duration = self.attack_duration / 2
        else:
            duration = self.attack_duration

        if (self.attack_timer.now > self.attack_duration):
            self.attack_timer.reset_timer()
            self.is_in_attack_mode = not self.is_in_attack_mode

        if self.is_in_attack_mode == False:
            actual_target = (randint(0, 700), randint(0, 100))
        else:
            actual_target = target


        self.acc = self.seek_with_approach(actual_target)
        # equations of motion
        super().update()
