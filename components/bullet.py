import pygame
import math
from components.entity import Entity
vec = pygame.math.Vector2

LAZER = (0, 255, 43)

class Bullet(Entity):
    """ represents Projectiles """

    def __init__(self, pos, *groups):
        super().__init__(pygame.Surface([4, 10], pygame.SRCALPHA), (2000, 100, 120), pos, groups)
        self.m_pos = pygame.mouse.get_pos()
        self.pos = vec(pos)
        des = self.pos - self.m_pos
        angle = math.atan2(des.x, des.y)
        angle %= 2*math.pi
        self.sound = pygame.mixer.Sound('assets/sounds/ship_lazer.ogg')
        self.image.fill(LAZER)
        self.image = pygame.transform.rotate(self.image, math.degrees(angle))
        self.acc = (self.m_pos - self.pos).normalize() * self.max_speed

        self.sound.play()

    def update(self, dt):
        """ move the bullet """

        super().update(dt)

        if self.rect.y < -50:
            self.kill()
