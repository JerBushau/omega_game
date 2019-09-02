import pygame
from components.weapon import Weapon
from components.bullet import Bullet
from components.entity import Entity
from components.chain_lightning import Chain_Lightning
from components.signaly import signaly
from helpers import angle_from_vec

WIDTH = 1050
HEIGHT = 600

vec = pygame.math.Vector2

PLAYER = pygame.image.load('assets/ship1.png')

class Player(Entity):
    """ represents the Player. """

    def __init__(self, *groups):
        super().__init__(pygame.transform.scale(PLAYER, (125, 125)), (200, 800, 120), (WIDTH/2, HEIGHT-50), groups)
        self.hp = 10
        self.mask = pygame.mask.from_surface(self.image, 200)
        self.image.fill((5, 5, 5, 10), special_flags=pygame.BLEND_RGB_ADD)
        self.rect = self.image.get_rect()
        self.weapon = Weapon(Bullet)
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
                signaly.emit('GAME_OVER')

                # self.done = True

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
        angle = angle_from_vec(des)
        img, rect = self.rot_center(self.image, self.rect, angle)
        rect.center = self.rect.center

        # rect.clamp_ip(screen.get_rect())
        screen.blit(img, rect)

    def move(self, direction):
        self.direction = direction

    def update(self, dt):
        """ update the player's position to the mouse x position """
        self.weapon.bullets.update(dt)
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


