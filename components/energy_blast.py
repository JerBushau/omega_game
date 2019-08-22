import pygame
from components.entity import Entity
from timer import Timer
from sprite_sheet_loader import sprite_sheet

WOBBLE = pygame.image.load('assets/wobble.png')
E_B = 'assets/hedgehog-proj.png'

class EnergyBlast(Entity):
    def __init__(self, pos, target, *groups):
        SHEET = sprite_sheet((32, 32), E_B)
        super().__init__(SHEET[0], (100, 100, 120), pos, groups)
        self.sheet = SHEET
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
            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (40, 40))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            if self.current_sprite_index == cap:
                self.current_sprite_index = 0

    def update(self, dt):
        self.sprite_animation()
        super().update(dt)

        if (self.rect.y <= -50
            or self.rect.y >= 450
            or self.rect.x <= 0
            or self.rect.x >= 700):
            self.kill()

