import pygame
from components.weapon import Weapon
from components.bullet import Bullet
from components.entity import Entity
from components.chain_lightning import Chain_Lightning
from components.signaly import signaly
from components.player_health_bar import PlayerHealthBar
from components.on_screen_dmg import OnScreenDmg
from sprite_sheet_loader import sprite_sheet
from timer import Timer
from helpers import angle_from_vec
from random import randint

WIDTH = 1050
HEIGHT = 600

vec = pygame.math.Vector2

PLAYER = pygame.image.load('assets/ship1.png')

class Player(Entity):
    """ represents the Player. """

    def __init__(self, *groups):
        SHEET = sprite_sheet((100,100), 'assets/ship-death.png')
        super().__init__(pygame.transform.scale(PLAYER, (125, 125)), (200, 800, 120), (WIDTH/2, HEIGHT-50), groups)
        self.hp = 6
        self.mask = pygame.mask.from_surface(self.image, 200)
        self.image.fill((5, 5, 5, 10), special_flags=pygame.BLEND_RGB_ADD)
        self.sheet = SHEET
        self.rect = self.image.get_rect()
        self.weapon = Weapon(Bullet)
        self.direction = 'stop'
        self.death_animation_timer = Timer(60)
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.current_sprite_index = 0
        self.dying = False
        self.post_death_timer = Timer(500)
        self.health_bar = PlayerHealthBar(self.hp)
        self.regen_cooldown_timer = Timer(50*100)
        self.regen_timer = Timer(500)

    def get_event(self, event, **state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            can_fire = self.weapon.ammo > 0 and not self.dying
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

    def collision_detected(self, hp_delta):
        self.hp -= hp_delta

        self.regen_timer.reset()
        self.regen_cooldown_timer.start()

    def handle_regen(self):
        if self.regen_cooldown_timer.is_finished():
            self.regen_timer.start_repeating()
            signaly.emit('PLAYER_MSSG', 'REGEN!')

        if self.regen_timer.is_finished():
            crit_roll = randint(1, 101)
            will_crit = crit_roll > 96
            if will_crit:
                amt = 0.15*10
            else:
                amt = 0.15
            if self.hp < self.health_bar.starting_hp and not self.dying:
                self.hp += amt
                signaly.emit('PLAYER_MSSG', amt)

        if self.hp == self.health_bar.starting_hp:
            # self.hp = self.health_bar.starting_hp
            self.regen_timer.reset()

    def explode(self):
        if not self.dying:
            self.destruction_sound.play()
            self.dying = True
            self.max_speed = 45
            self.death_animation_timer.start_repeating()
            self.weapon.cease_fire()
            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (125, 125))
        
    def sprite_animation(self):
        cap = 11

        if (self.death_animation_timer.is_finished()):
            self.current_sprite_index+=1

            if self.current_sprite_index == cap-1:
                self.post_death_timer.start()
            elif self.current_sprite_index >= cap:
                self.current_sprite_index = cap
                

            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (125, 125))

    def draw(self, screen):
        """ draw player specifically """
        mouse_pos = pygame.mouse.get_pos()
        des = self.pos - vec(mouse_pos)
        angle = angle_from_vec(des)
        img, rect = self.rot_center(self.image, self.rect, angle)
        rect.center = self.rect.center

        screen.blit(img, rect)

    def move(self, direction):
        self.direction = direction

    def update(self, dt):
        """ update the player's position to the mouse x position """
        self.handle_regen()
        self.sprite_animation()
        self.weapon.bullets.update(dt)
        self.health_bar.update(self.hp)


        if self.post_death_timer.is_finished():
            self.kill()
            signaly.remove_subscriber('PLAYER_MSSG')
            signaly.emit('GAME_OVER')

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


