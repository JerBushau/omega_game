import pygame
from timer import Timer

WIDTH = 1050
HEIGHT = 600

def text_objects(text, font, color):
    """Creates 'text objects' for displaying messages"""
    text_surf = font.render(text, True, color)
    return text_surf, text_surf.get_rect()

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, hp, dimentions, pos, font={'face': 'freesansbold.ttf', 'size': 8}, colors=((255,70,70), (153,42,42), (30,8,8))):
        super().__init__()
        self.starting_hp = hp
        self.width = dimentions[0]
        self.height = dimentions[1]
        self.foreground_color = colors[0]
        self.temp_color = colors[1]
        self.background_color = colors[2]
        self.current_hp = hp
        self.background = pygame.Surface([self.width, self.height])
        self.foreground = pygame.Surface([self.width, self.height])
        self.background.fill(self.background_color)
        self.foreground.fill(self.foreground_color)
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.font = font
        if font != None:
            self.font = font['face']
            self.font_size = font['size']
            t_surf, t_rect = text_objects('{}/{}'.format(self.current_hp, self.starting_hp), pygame.font.Font(self.font, self.font_size), (255, 255, 255))
            self.foreground.blit(t_surf, t_rect)
        self.image.blit(self.foreground, (0, 0))
        self.rect.center = pos or (WIDTH/2, -10)
        self.total_dmg = 0
        self.temp_timers = []

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, hp):
        self.current_hp = hp
        self.prev_width = self.foreground.get_width()
        foreground_width = int(max(min(self.current_hp / float(self.starting_hp) * self.width, self.width), 0))
        diff = self.prev_width - foreground_width
        self.total_dmg += diff

        def remove_temp():
            self.total_dmg -= diff

        temp_timer = Timer(500, cb=remove_temp)
        temp_timer.start()
        self.temp_timers.append(temp_timer)

        for t in self.temp_timers:
            t.is_finished()

        self.foreground = pygame.Surface([foreground_width, self.height])
        self.foreground.fill(self.foreground_color)
        self.background.fill(self.background_color)

        if self.font != None:
            t_surf, t_rect = text_objects('{}/{}'.format(self.current_hp, self.starting_hp), pygame.font.Font(self.font, self.font_size), (255, 255, 255))
            middle_of_bar = self.width/2

            if self.foreground.get_width() - t_surf.get_width() > middle_of_bar:
                text_pos = (middle_of_bar, 0)
            else:
                text_pos = (self.foreground.get_width() - t_surf.get_width() -10, 0)

            self.foreground.blit(t_surf, text_pos)

        self.background.blit(self.foreground, self.background.get_rect())

        if self.total_dmg > 0:
            temp = pygame.Surface([self.total_dmg, self.height])
            temp.fill(self.temp_color)
            self.background.blit(temp, (foreground_width, 0))

        self.image = self.background
