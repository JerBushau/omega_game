import pygame
import random
from components.entity import Entity

vec = pygame.math.Vector2

def text_objects(text, font, color):
    """Creates 'text objects' for displaying messages"""
    text_surf = font.render(text, True, color)
    return text_surf, text_surf.get_rect()

WIDTH = 1050
HEIGHT = 600

class Mssg(Entity):
    def __init__(self, text, color, pos=((WIDTH/2), -20), font_size=17, *groups):
        super().__init__(pygame.Surface([0, 0]), (200, 100, 120), pos, groups)
        large_text = pygame.font.Font('./assets/fonts/Sansation-Bold.ttf', font_size)
        self.starting_pos = pos
        self.image, self.rect = text_objects(text, large_text, color)
        self.rect.center = pos
        self.max_speed = 400
        self.dies_off_screen = True
        alpha_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        alpha_image.fill((255, 255, 255, color[3]))
        self.image.blit(alpha_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self, dt):
        super().update(dt)

        if self.dies_off_screen:
            if (self.rect.y <= -50
                or self.rect.y >= HEIGHT + 50
                or self.rect.x <= 0
                or self.rect.x >= WIDTH):
                self.kill()


