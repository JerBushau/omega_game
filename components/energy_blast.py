import pygame
from components.entity import Entity
from timer import Timer
from sprite_sheet_loader import sprite_sheet

E_B = 'assets/hedgehog-proj.png'
WIDTH = 1050
HEIGHT = 600

class EnergyBlast(Entity):
    def __init__(self, pos, target, seeking=False, *groups):
        SHEET = sprite_sheet((32, 32), E_B)
        super().__init__(SHEET[0], (450, 550, 120), pos, groups)
        self.sheet = SHEET
        self.sprite_animation_timer = Timer(100)
        self.current_sprite_index = 0
        self.target = target
        if seeking:
            self.acc = self.seek(target)
        else:
            self.acc = target
        self.sprite_animation_timer.start_repeating()

    def sprite_animation(self):
        cap = 4
        if self.sprite_animation_timer.is_finished() and self.current_sprite_index < cap:
            self.current_sprite_index += 1
            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (50, 50))
            self.image.convert()
            self.mask = pygame.mask.from_surface(self.image, 200)
            self.rect = self.image.get_rect()
            if self.current_sprite_index == cap:
                self.current_sprite_index = 0

    def update(self, dt):
        self.sprite_animation()
        super().update(dt)

        if (self.rect.y <= -50
            or self.rect.y >= HEIGHT + 50
            or self.rect.x <= -32
            or self.rect.x >= WIDTH):
            self.kill()

