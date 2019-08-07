import pygame

class Hud(pygame.sprite.Sprite):
    """ represents the HUD elements """

    # maybe take a named tuple or dict as arg here or something
    def __init__(self, x, y, width, height, label,  delimiter=':', small=False):
        super().__init__()

        if  small:
            self.HUD_ITEM = pygame.image.load('assets/HUD_item_small.png')
            self.HUD_ITEM = pygame.transform.scale(self.HUD_ITEM, (width, height))

        else:
            self.HUD_ITEM = pygame.image.load('assets/HUD_item.png')
            self.HUD_ITEM = pygame.transform.scale(self.HUD_ITEM, (width, height))

        self.image = self.HUD_ITEM.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.label = label
        self.delimiter = delimiter

    # should probably fix this to work with update now
    def update(self, dest=None):
        """ Update the hud info """

        font = pygame.font.Font('freesansbold.ttf',15)
        self.image = self.HUD_ITEM.convert_alpha()
        self.text = font.render('{}{} {}'
            .format(self.label, self.delimiter, self.prop), True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = ((self.text_rect.x + (self.width/2),
                                (self.text_rect.y + (self.height/2))))
        
        self.image.blit(self.text, self.text_rect)

        if dest:
            dest.blit(self.image, self.rect)
