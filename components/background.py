import pygame

WIDTH = 1050
HEIGHT = 600

class Background(pygame.sprite.Sprite):
    """ represents the background image """

    def __init__(self, image_file, location):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(image_file), (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
