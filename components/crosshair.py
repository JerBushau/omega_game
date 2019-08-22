import pygame
from timer import Timer
from sprite_sheet_loader import sprite_sheet

vec = pygame.math.Vector2

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.last_m_pos = None
        self.m_pos = pygame.mouse.get_pos()
        self.sheet = sprite_sheet((21,21), 'assets/crosshair.png')
        self.current_sprite_index = 0
        self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = self.m_pos
        self.animation ='grow'

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.last_m_pos = self.m_pos;
        self.m_pos = pygame.mouse.get_pos()
        self.rect.center = self.m_pos

        diff = vec(self.last_m_pos) - vec(self.m_pos)
        
        if self.animation =='grow':
            self.current_sprite_index += 1
        elif self.animation == 'shrink':
            self.current_sprite_index -= 1
        if self.current_sprite_index > 4:
            self.current_sprite_index = 4
        if self.current_sprite_index < 0:
            self.current_sprite_index = 0

        if (diff.length() > 0.15):
            self.animation = 'grow'
        else:
            self.animation = 'shrink'

        self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (30, 30))
        

