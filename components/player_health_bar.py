import pygame
from timer import Timer
from components.health_bar import HealthBar

WIDTH = 1050
HEIGHT = 600

class PlayerHealthBar(HealthBar):
    def __init__(self, hp):
        super().__init__(hp, (150, 15), (WIDTH-85, HEIGHT+25), 
                         font=None, 
                         colors=((0,135,236, 100), (0,81,141, 100), (0,13,23))
                        )
        self.down_timer = Timer(1200)
        self.direction = 'up'

    def update(self, hp):
        super().update(hp)

        if self.rect.y > HEIGHT-25 and self.current_hp > 0:
            self.rect.y -= 1

        if self.direction == 'down':
            self.rect.y +=1

        if self.current_hp <= 0 and not self.down_timer.is_active:
            self.down_timer.start()

        if self.down_timer.is_finished():
            self.direction = 'down'
        