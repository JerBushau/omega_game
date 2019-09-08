import pygame
from timer import Timer

WIDTH = 1050
HEIGHT = 600

def text_objects(text, font, color):
    """Creates 'text objects' for displaying messages"""
    text_surf = font.render(text, True, color)
    return text_surf, text_surf.get_rect()

class BossHealthBar(pygame.sprite.Sprite):
    def __init__(self, hp):
        super().__init__()
        self.starting_hp = hp
        self.current_hp = hp
        self.background = pygame.Surface([975, 7])
        self.foreground = pygame.Surface([975, 7])
        self.background.fill((0,0,0))
        self.foreground.fill((255, 51, 51))
        self.image = pygame.Surface([975, 7])
        self.rect = self.image.get_rect()
        t_surf, t_rect = text_objects('{}/{}'.format(self.current_hp, self.starting_hp), pygame.font.Font('freesansbold.ttf', 7), (255, 255, 255))
        self.foreground.blit(t_surf, t_rect)
        self.image.blit(self.foreground, (0, 0))
        self.rect.center = (WIDTH/2, -10)
        self.up_timer = Timer(1200)
        self.total_dmg = 0
        self.direction = 'down'
        self.temp_timers = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, hp):
        self.current_hp = hp
        self.prev_width = self.foreground.get_width()
        foreground_width = int(max(min(self.current_hp / float(self.starting_hp) * 975, 975), 0))
        diff = self.prev_width - foreground_width
        self.total_dmg += diff

        def remove_temp():
            self.total_dmg -= diff

        temp_timer = Timer(1000, cb=remove_temp)
        temp_timer.start()
        self.temp_timers.append(temp_timer)

        for t in self.temp_timers:
            t.is_finished()

        temp = pygame.Surface([self.total_dmg, 7])
        self.foreground = pygame.Surface([foreground_width, 7])
        self.foreground.fill((181, 10, 22))
        self.background.fill((20,20,20))
        temp.fill((255,0,0))

        t_surf, t_rect = text_objects('{}/{}'.format(self.current_hp, self.starting_hp), pygame.font.Font('freesansbold.ttf', 7), (255, 255, 255))
        middle_of_bar = 975/2

        if self.foreground.get_width() - t_surf.get_width() > middle_of_bar:
            text_pos = (middle_of_bar, 0)
        else:
            text_pos = (self.foreground.get_width() - t_surf.get_width() -10, 0)

        self.foreground.blit(t_surf, text_pos)
        self.background.blit(self.foreground, self.background.get_rect())
        self.background.blit(temp, (foreground_width, 0))
        self.image = self.background

        if self.rect.y < 10 and self.current_hp > 0:
            self.rect.y += 1

        if self.direction == 'up':
            self.rect.y -=1

        if self.current_hp <= 0 and not self.up_timer.is_active:
            self.up_timer.start()

        if self.up_timer.is_finished():
            self.direction = 'up'
