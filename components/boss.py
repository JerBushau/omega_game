import pygame
from random import randint, uniform, choice
from components.entity import Entity
from timer import Timer
from components.weapon import Weapon
from components.bullet import Bullet
from sprite_sheet_loader import sprite_sheet

vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400

ENEMY = pygame.image.load('assets/space-hedgehog.png')
DESTRO_ENEMY = pygame.image.load('assets/space-hedgehog.png')

class Boss(Entity):
    """Boss entity"""

    def __init__(self, s_pos=(-30, -30), *groups):
        super().__init__(pygame.transform.scale(ENEMY.convert_alpha(), (80, 80)), (200, 200, 120), s_pos, groups)
        self.hp = 600
        self.sheet = sprite_sheet((32,32), 'assets/space_hedgehog_sheet.png');
        self.sprite_animation = Timer(120)
        self.current_sprite_index = 0
        self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (80, 80))
        self.is_in_attack_mode = False
        self.attack_duration = 5000
        self.attack_timer = Timer(self.attack_duration)
        self.death_animation_timer = Timer(6000)
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.hit = False
        self.return_point = choice([(500, 100), (50, 200), (350, 100)])
        self.weapon = Weapon(Bullet)

        self.sprite_animation.start_repeating()

    def explode(self):
        """ mark enemy as hit """

        self.hit = True
        self.max_speed = 75
        self.destruction_sound.play()
        self.death_animation_timer.start()


    def death_animation(self):
        """Enemy movement once marked as hit"""

        if self.death_animation_timer.is_finished():
            self.kill()
        else:
            self.acc = self.seek((self.pos.x, HEIGHT + 40))


    def basic_animation(self):
        cap = 4
        if self.hit:
            self.sheet = sprite_sheet((32, 32), 'assets/dedgehog_sheet.png')
            self.sprite_animation.set_duration(250)
            cap = 12
        if self.sprite_animation.is_finished() and self.current_sprite_index < cap:
            self.current_sprite_index+=1
            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (80, 80))
            if self.current_sprite_index == cap:
                if cap == 12:
                    self.current_sprite_index = cap
                else:
                    self.current_sprite_index = 0


    def update(self, dt, target):
        self.basic_animation()


        if not self.attack_timer.is_active:
            self.attack_timer.start()

        if self.is_in_attack_mode == True:
            self.attack_timer.set_duration(self.attack_duration / 1.8)
        else:
            self.attack_timer.set_duration(self.attack_duration)

        if self.attack_timer.is_finished():
            self.is_in_attack_mode = not self.is_in_attack_mode
            self.return_point = choice([(600, 100), (100, 200), (350, 90)])

        if self.is_in_attack_mode == False:
            actual_target = self.return_point
        else:
            actual_target = target

        self.acc = self.seek_with_approach(actual_target)

        if self.death_animation_timer.is_active and self.hit:
            self.death_animation()
        super().update(dt)
