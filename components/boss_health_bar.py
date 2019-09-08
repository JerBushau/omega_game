import pygame
from timer import Timer
from components.health_bar import HealthBar

WIDTH = 1050
HEIGHT = 600

class BossHealthBar(HealthBar):
    def __init__(self, hp):
        super().__init__(hp, (975, 8), None)
        self.up_timer = Timer(1200)
        self.direction = 'down'

    def update(self, hp):
        super().update(hp)
        
        if self.rect.y < 10 and self.current_hp > 0:
            self.rect.y += 1

        if self.direction == 'up':
            self.rect.y -=1

        if self.current_hp <= 0 and not self.up_timer.is_active:
            self.up_timer.start()

        if self.up_timer.is_finished():
            self.direction = 'up'
