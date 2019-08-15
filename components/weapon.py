import pygame
from timer import Timer2

class Weapon:
    
    def __init__(self, ammo_type):
        self.is_firing = False
        self.firing_timer = Timer2(180)
        self.ammo_type = ammo_type


    def begin_fire(self):
        self.is_firing = True
        self.firing_timer.start_repeating()


    def cease_fire(self):
        self.is_firing = False
        self.firing_timer.reset()