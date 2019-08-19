import pygame
import math
from components.weapon import Weapon
from components.bullet import Bullet
from components.entity import Entity
from components.chain_lightning import Chain_Lightning

HEIGHT = 400
WIDTH = 700

vec = pygame.math.Vector2

PLAYER = pygame.image.load('assets/ship.png')

class Player(Entity):
    """ represents the Player. """

    def __init__(self):
        super().__init__(PLAYER, (200, 800, 120))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.weapon = Weapon(Bullet)
        self.pos = (WIDTH / 2, HEIGHT - 40)
        self.direction = 'stop'

    def get_event(self, event, **state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            can_fire = self.weapon.ammo > 0
            if can_fire and event.button == 1:
                self.weapon.begin_fire(self.rect.center)
                state['shots_fired'] += 1

            elif can_fire and event.button == 3:
                for i in range(3):
                    bullet = Chain_Lightning(self.rect.center, self.weapon.bullets)
                    bullet.find_next_target(state['enemy_list'].sprites() + state['boss_list'].sprites())
                    state['shots_fired'] += 1
                    self.weapon.ammo -= 1

            elif event.button == 2:
                self.weapon.ammo += 30

            elif not can_fire:
                print('you loose')
                pygame.mixer.music.fadeout(1000)
                # message_display('YOU LOOSE OUT OF AMMO!!!', WHITE, pygame.display.get_surface(), (700, 400))

                self.done = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.weapon.cease_fire()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move('left')

            if event.key == pygame.K_d:
                self.move('right')

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.move('stop')

            if event.key == pygame.K_d:
                self.move('stop')


    def draw(self, screen):
        """ draw player specifically """
        mouse_pos = pygame.mouse.get_pos()
        des = self.pos - vec(mouse_pos)
        angle = math.atan2(des.x, des.y)
        angle%=2*math.pi
        img = self.rot_center(self.image, math.degrees(angle))
        rect = img.get_rect()
        rect.center = self.rect.center

        # rect.clamp_ip(screen.get_rect())
        screen.blit(img, rect)

    def move(self, direction):
        self.direction = direction

    def update(self, dt):
        """ update the player's position to the mouse x position """

        if self.direction == 'left':
            self.acc = vec(-1, 0).normalize() * self.max_speed
        elif self.direction == 'right':
            self.acc = vec(701, 0).normalize() * self.max_speed
        elif self.direction == 'stop':
            self.acc = vec(0 ,0)

        # give edges of screen a little bounce when hit
        if self.pos[0] >= (WIDTH -30):
            self.pos[0] = WIDTH -30
            self.acc = vec(-1, 0).normalize() * 2000
        elif self.pos[0] <= 30:
            self.pos[0] = 30
            self.acc = vec(701, 0).normalize() * 2000

        super().update(dt)


