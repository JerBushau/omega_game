import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font=None, text='', text_color=(0, 0, 0),
                 image_normal=pygame.Surface([100, 40], pygame.SRCALPHA), image_hover=pygame.Surface([100, 40], pygame.SRCALPHA),
                 image_down=pygame.Surface([100, 40], pygame.SRCALPHA)):
        super().__init__()
        # Scale the images to the desired size (doesn't modify the originals).
        self.image_normal = pygame.transform.scale(image_normal, (width, height))
        self.image_hover = pygame.transform.scale(image_hover, (width, height))
        self.image_down = pygame.transform.scale(image_down, (width, height))

        self.image = self.image_normal  # The currently active image.
        self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)
        # Blit the text onto the images.
        self.image_normal.fill((0, 140, 250))
        self.image_hover.fill((10, 100, 250))
        self.image_down.fill((0, 50, 140))
        for image in (self.image_normal, self.image_down, self.image_hover):
            image.blit(text_surf, text_rect)

        # This function will be called when the button gets pressed.
        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):

                self.image = self.image_down
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()  # Call the function.
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal
