import pygame
from timer import Timer

class Weapon:

    def __init__(self, ammo_type):
        self.is_firing = False
        self.cooldown_timer = Timer(200)
        self.ammo_type = ammo_type
        self.ammo = 1000
        self.bullets = pygame.sprite.Group()


    def begin_fire(self, pos):
        self.is_firing = True
        self.fire(pos, True)
        self.cooldown_timer.start_repeating()

    def fire(self, pos, first_shot=False):
        if (first_shot
        or (self.cooldown_timer.is_finished()
        and self.ammo > 0)):
            self.ammo_type(pos, self.bullets)
            self.ammo -= 1

    def cease_fire(self):
        self.is_firing = False
        self.cooldown_timer.reset()

    def bullet_collisions(self, **targets):
        pass
