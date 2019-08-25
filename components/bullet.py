import pygame
from components.entity import Entity
from helpers import angle_from_vec
vec = pygame.math.Vector2

LAZER = (0, 255, 43)
WIDTH = 1050
HEIGHT = 600

class Bullet(Entity):
    """ represents Projectiles """

    def __init__(self, pos, *groups):
        super().__init__(pygame.Surface([2, 12], pygame.SRCALPHA), (2000, 100, 120), pos, groups)
        self.m_pos = pygame.mouse.get_pos()
        self.sound = pygame.mixer.Sound('assets/sounds/ship_lazer.ogg')
        self.image.fill(LAZER)
        self.mask = pygame.mask.from_surface(self.image)
        desired_vec = self.pos - self.m_pos
        self.image = pygame.transform.rotate(self.image, angle_from_vec(desired_vec))
        self.acc = (self.m_pos - self.pos).normalize() * self.max_speed

        self.sound.play()

    def update(self, dt):
        """ move the bullet """

        super().update(dt)

        if (self.rect.y <= -50
            or self.rect.y >= HEIGHT + 50
            or self.rect.x <= 0
            or self.rect.x >= WIDTH):
            self.kill()



