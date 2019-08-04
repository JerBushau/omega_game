import pygame
from bullet import Bullet

WOBBLE = pygame.image.load('assets/wobble.png')


class Wobble_shot(Bullet):

    def __init__(self, pos):
        super().__init__(pos)
        self.image = WOBBLE.convert_alpha()
        self.wobble = 'right'
        self.speed = 2
        self.x_origin = pos[0]

    # def explode(self):

    def grow_animation(self):
        # get rid of magic numbers here!
        # expansion_point = 250 or something
        # maybe make self.expand_point and self.expand_cap
        if self.rect.y < 250:
            growth = 250 - self.rect.y
            cap = 30
            if growth < cap:
                self.image = pygame.transform.scale(WOBBLE.convert_alpha(), (growth, growth))

            elif growth >= cap:
                self.rect.height, self.rect.width = 15, 15

    def wobble_animation(self):
        delta = 10
        diff = self.x_origin - self.rect.x

        if self.wobble == 'right':
            self.rect.x += 2
        else:
            self.rect.x -= 2

        if diff < -delta:
            self.wobble = 'left'
        elif diff > delta:
            self.wobble = 'right'


    def update(self):

        super().update()

        self.wobble_animation()
        self.grow_animation()
