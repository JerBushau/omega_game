import pygame
import random
from sprite_sheet_loader import sprite_sheet

ASTEROID = 'assets/asteroid.png'


class Asteroid_group(pygame.sprite.Group):
    """ custom group to make use of asteroids custom job """
    def __init__(self):
        super().__init__()

    def draw(self, screen):
        sprites = self.sprites()
        for spr in sprites:
            spr.draw(screen)


class Asteroid(pygame.sprite.Sprite):
    """ represents the asteroids """

    def __init__(self, size, hp):
        super().__init__()

        y_starting_pos = random.randrange(60, 100) * -1
        x_starting_pos = random.randrange(1, 700)

        self.sheet = sprite_sheet((64,64), ASTEROID)
        self.image =  self.sheet[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect_img = self.image.get_rect()
        self.rect_img.x = x_starting_pos
        self.rect_img.y = y_starting_pos
        self.rect = self.rect_img.copy()
        self.size = size
        self.speed = random.randrange(1, 6)
        self.hp = hp

    def draw(self, screen):
        """ draws the asteroids with new image based on hp"""

        if self.hp < 5:
            self.image = self.sheet[6]

        elif self.hp < 10:
            self.image = self.sheet[5]

        elif self.hp < 12:
            self.image = self.sheet[4]

        elif self.hp < 14:
            self.image = self.sheet[3]

        elif self.hp < 16:
            self.image = self.sheet[2]

        elif self.hp < 18:
            self.image = self.sheet[1]

        self.mask = pygame.mask.from_surface(self.image)

        if self.hp > 0:
            screen.blit(self.image, self.rect_img)

    def update(self):
        """ update the asteroids's position """

        self.rect_img.y += self.speed

        if self.rect_img.y > 460:
            self.rect_img.y = random.randrange(60, 100) * -1
            self.rect_img.x = random.randrange(1, 700)

        self.rect.center = self.rect_img.center
        # current_ticks = pygame.time.get_ticks()

        if self.hp <= 0:
            self.kill()
