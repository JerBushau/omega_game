import pygame

LAZER = (0, 255, 43)

class Bullet(pygame.sprite.Sprite):
    """ represents Projectiles """

    def __init__(self, pos):
        super().__init__()
        self.sound = pygame.mixer.Sound('assets/sounds/ship_lazer.ogg')
        self.height = 10
        self.width = 4
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(LAZER)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 5

        self.sound.play()

    def update(self):
        """ move the bullet """

        self.rect.y -= self.speed

