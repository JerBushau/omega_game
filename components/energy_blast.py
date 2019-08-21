import pygame
from components.entity import Entity
from timer import Timer
from sprite_sheet_loader import sprite_sheet

WOBBLE = pygame.image.load('assets/wobble.png')
E_B = 'assets/hedgehog-proj.png'

class EnergyBlast(Entity):

    def __init__(self, pos, target, *groups):
        super().__init__(WOBBLE, (100, 100, 120), pos, groups)
        self.sheet = sprite_sheet((32, 32), E_B)
        self.sprite_animation_timer = Timer(100)
        self.current_sprite_index = 0
        # self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (50, 50))
        # self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.target = target
        self.acc = self.seek_with_approach(target)

        self.sprite_animation_timer.start_repeating()

    def sprite_animation(self):
        cap = 4
        if self.sprite_animation_timer.is_finished() and self.current_sprite_index < cap:
            self.current_sprite_index += 1
            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (50, 50))
            self.rect = self.image.get_rect()
            if self.current_sprite_index == cap:
                self.current_sprite_index = 0

    def update(self, dt):
        super().update(dt)
        self.sprite_animation()


